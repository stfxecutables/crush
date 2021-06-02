import nipype.interfaces.io as nio  # Data i/o
import nipype.interfaces.fsl as fsl  # fsl
import nipype.interfaces.diffusion_toolkit as dtk
import nipype.interfaces.utility as util  # utility
import nipype.pipeline.engine as pe  # pypeline engine
import os  # system functions
#from niflow.nipype1.workflows.dmri.fsl.dti import create_eddy_correct_pipeline
from nipype.workflows.dmri.preprocess.epi import ecc_pipeline as create_eddy_correct_pipeline

from nipype.utils.misc import package_check

package_check('numpy', '1.3', 'tutorial1')
package_check('scipy', '0.7', 'tutorial1')
package_check('IPython', '0.10', 'tutorial1')

subject_list = ['Tractography']

info = dict(
    dwi=[['subject_id', 'Tractography']],
    bvecs=[['subject_id', 'sub-A00000300_ses-20110101_run-01_dwi.bvec']],
    bvals=[['subject_id', 'sub-A00000300_ses-20110101_run-01_dwi.bval']])

infosource = pe.Node(
    interface=util.IdentityInterface(fields=['subject_id']), name="infosource")

infosource.iterables = ('subject_id', subject_list)

datasource = pe.Node(
    interface=nio.DataGrabber(
        infields=['subject_id'], outfields=list(info.keys())),
    name='datasource')

datasource.inputs.template = "%s/%s"

# This needs to point to the fdt folder you can find after extracting
# http://www.fmrib.ox.ac.uk/fslcourse/fsl_course_data2.tar.gz
datasource.inputs.base_directory = os.path.abspath('/home/dmattie/scratch/sub-A00000300/ses-20110101/Tractography')

datasource.inputs.field_template = dict(dwi='%s/%s.nii')
datasource.inputs.template_args = info
datasource.inputs.sort_filelist = True

compute_ODF = pe.Workflow(name='compute_ODF')

fslroi = pe.Node(interface=fsl.ExtractROI(), name='fslroi')
fslroi.inputs.t_min = 0
fslroi.inputs.t_size = 1

bet = pe.Node(interface=fsl.BET(), name='bet')
bet.inputs.mask = True
bet.inputs.frac = 0.34

eddycorrect = create_eddy_correct_pipeline('eddycorrect')
eddycorrect.inputs.inputnode.ref_num = 0

hardi_mat = pe.Node(interface=dtk.HARDIMat(), name='hardi_mat')

odf_recon = pe.Node(interface=dtk.ODFRecon(), name='odf_recon')

compute_ODF.connect(
    [(fslroi, bet, [('roi_file', 'in_file')]),
     (eddycorrect, odf_recon, [('outputnode.eddy_corrected', 'DWI')]),
     (eddycorrect, hardi_mat,
      [('outputnode.eddy_corrected',
        'reference_file')]), (hardi_mat, odf_recon, [('out_file', 'matrix')])])

tractography = pe.Workflow(name='tractography')

odf_tracker = pe.Node(interface=dtk.ODFTracker(), name="odf_tracker")

smooth_trk = pe.Node(interface=dtk.SplineFilter(), name="smooth_trk")
smooth_trk.inputs.step_length = 1

tractography.connect([(odf_tracker, smooth_trk, [('track_file',
                                                  'track_file')])])

dwiproc = pe.Workflow(name="dwiproc")
dwiproc.base_dir = os.path.abspath('dtk_odf_tutorial')
dwiproc.connect([(infosource, datasource, [('subject_id', 'subject_id')]),
                 (datasource, compute_ODF,
                  [('dwi', 'fslroi.in_file'), ('bvals', 'hardi_mat.bvals'),
                   ('bvecs', 'hardi_mat.bvecs'),
                   ('dwi', 'eddycorrect.inputnode.in_file')]),
                 (compute_ODF, tractography,
                  [('bet.mask_file', 'odf_tracker.mask1_file'),
                   ('odf_recon.ODF', 'odf_tracker.ODF'),
                   ('odf_recon.max', 'odf_tracker.max')])])

dwiproc.inputs.compute_ODF.hardi_mat.oblique_correction = True
dwiproc.inputs.compute_ODF.odf_recon.n_directions = 31
dwiproc.inputs.compute_ODF.odf_recon.n_b0 = 5
dwiproc.inputs.compute_ODF.odf_recon.n_output_directions = 181

if __name__ == '__main__':
    dwiproc.run()
    dwiproc.write_graph()                                                  