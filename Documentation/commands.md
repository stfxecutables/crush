
##AWS CLI

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip

./aws/install --install-dir ~/.local/aws-cli --bin-dir ~/.local/bin

You can now rm -r ~/aws/ and the zip file

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration

aws s3 sync s3://hcp-openaccess/HCP/101006/T1w ~/projects/def-dmattie/HCP/101006/T1w


 mri_convert -rt nearest -nc -ns 1 brainmask.mgz brainmask.nii

## Postgresql

psql --dbname=crush --password

