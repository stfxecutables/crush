T = readtable('2019-06-07.mid.csv');
%T = readtable('/media/dmattie/GENERAL/HCP/Analysis/csv-dataframe2.csv/csv-dataframe2.csv');

%%ProcessLoadedFile

%[Gender,GenderNames]=findgroups(T.Gender);

%TavgTractsToRenderASYMByGender = table;
%avgTractsToRenderASYMByGender = splitapply(meanOmitNan,T.TractsToRender_asymidx,Gender);
%TavgTractsToRenderASYMByGender.Gender = GenderNames;
%TavgTractsToRenderASYMByGender.Average = avgTractsToRenderASYMByGender;

tempT=table;
tempT.meanFA_asymidx = str2double(T.meanFA_asymidx);
tempT.stddevFA_asymidx = str2double(T.stddevFA_asymidx);
tempT.meanADC_asymidx = str2double(T.meanADC_asymidx);
tempT.stddevADC_asymidx = str2double(T.stddevADC_asymidx);

%T.meanFA_asymidx = tempT.meanFA_asymidx;
%T.stddevFA_asymidx = tempT.stddevFA_asymidx;
%T.meanADC_asymidx = tempT.meanADC_asymidx;
%T.stddevADC_asymidx = tempT.stddevADC_asymidx;

meanOmitNan = @(x) mean(x,'omitNan');
Assymmetry = table;
[perGenderROI,Gender,ROILabel]=findgroups(T.Gender,T.ROILabel);

avgNumTractsASYM_perGenderROI = splitapply(meanOmitNan,T.NumTracts_asymidx,perGenderROI);
avgTractsToRenderASYM_perGenderROI = splitapply(meanOmitNan,T.TractsToRender_asymidx,perGenderROI);
avgLinesToRenderASYM_perGenderROI = splitapply(meanOmitNan,T.LinesToRender_asymidx,perGenderROI);
avgMeanTractLenASYM_perGenderROI = splitapply(meanOmitNan,T.MeanTractLen_asymidx,perGenderROI);
avgVoxelSizeXASYM_perGenderROI = splitapply(meanOmitNan,T.VoxelSizeX_asymidx,perGenderROI);
avgVoxelSizeYASYM_perGenderROI = splitapply(meanOmitNan,T.VoxelSizeY_asymidx,perGenderROI);
avgVoxelSizeZASYM_perGenderROI = splitapply(meanOmitNan,T.VoxelSizeZ_asymidx,perGenderROI);
avgmeanFAASYM_perGenderROI = splitapply(meanOmitNan,T.meanFA_asymidx,perGenderROI);
avgstddevFAASYM_perGenderROI = splitapply(meanOmitNan,T.stddevFA_asymidx,perGenderROI);
avgmeanADCASYM_perGenderROI = splitapply(meanOmitNan,T.meanADC_asymidx,perGenderROI);
avgstddevADCASYM_perGenderROI = splitapply(meanOmitNan,T.stddevADC_asymidx,perGenderROI);

avgNumTracts_perGenderROI = splitapply(meanOmitNan,T.NumTracts_asymidx,perGenderROI);
avgTractsToRender_perGenderROI = splitapply(meanOmitNan,T.TractsToRender_asymidx,perGenderROI);
avgLinesToRender_perGenderROI = splitapply(meanOmitNan,T.LinesToRender_asymidx,perGenderROI);
avgMeanTractLen_perGenderROI = splitapply(meanOmitNan,T.MeanTractLen_asymidx,perGenderROI);
avgVoxelSizeX_perGenderROI = splitapply(meanOmitNan,T.VoxelSizeX_asymidx,perGenderROI);
avgVoxelSizeY_perGenderROI = splitapply(meanOmitNan,T.VoxelSizeY_asymidx,perGenderROI);
avgVoxelSizeZ_perGenderROI = splitapply(meanOmitNan,T.VoxelSizeZ_asymidx,perGenderROI);
avgmeanFA_perGenderROI = splitapply(meanOmitNan,T.meanFA_asymidx,perGenderROI);
avgstddevFA_perGenderROI = splitapply(meanOmitNan,T.stddevFA_asymidx,perGenderROI);
avgmeanADC_perGenderROI = splitapply(meanOmitNan,T.meanADC_asymidx,perGenderROI);
avgstddevADC_perGenderROI = splitapply(meanOmitNan,T.stddevADC_asymidx,perGenderROI);

Assymmetry.Gender=Gender;
Assymmetry.ROILabel=ROILabel;

Assymmetry.NumTracts = avgTractsToRenderASYM_perGenderROI;
Assymmetry.LinesToRender = avgLinesToRenderASYM_perGenderROI;
Assymmetry.MeanTractLen  =avgLinesToRenderASYM_perGenderROI;
Assymmetry.VoxelSizeX = avgVoxelSizeXASYM_perGenderROI;
Assymmetry.VoxelSizeY = avgVoxelSizeYASYM_perGenderROI;
Assymmetry.VoxelSizeZ = avgVoxelSizeZASYM_perGenderROI;
Assymmetry.meanFA = avgmeanFAASYM_perGenderROI;
Assymmetry.stddevFA = avgstddevFAASYM_perGenderROI;
Assymmetry.meanADC = avgmeanADCASYM_perGenderROI;
Assymmetry.stddevADC = avgstddevADCASYM_perGenderROI;

Assymmetry.NumTracts_asymidx = avgTractsToRenderASYM_perGenderROI;
Assymmetry.LinesToRender_asymidx = avgLinesToRenderASYM_perGenderROI;
Assymmetry.MeanTractLen_asymidx  =avgLinesToRenderASYM_perGenderROI;
Assymmetry.VoxelSizeX_asymidx = avgVoxelSizeXASYM_perGenderROI;
Assymmetry.VoxelSizeY_asymidx = avgVoxelSizeYASYM_perGenderROI;
Assymmetry.VoxelSizeZ_asymidx = avgVoxelSizeZASYM_perGenderROI;
Assymmetry.meanFA_asymidx = avgmeanFAASYM_perGenderROI;
Assymmetry.stddevFA_asymidx = avgstddevFAASYM_perGenderROI;
Assymmetry.meanADC_asymidx = avgmeanADCASYM_perGenderROI;
Assymmetry.stddevADC_asymidx = avgstddevADCASYM_perGenderROI;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%assess the effect size (d=(mean1-mean2)/std), where mean1 is the mean of 
%the males and mean2 is the mean of the females and std is the standard 
%deviation of the joint distribution. There would be one for each of the 
%800K measurements. We have a lot of measurements here, we will probably 
%want all d values in an excel file and a basic summary: here are the 
%measurements (leading 10 to start) for the d statistic (both most negative 
%and most positive) comparing males and females with those measurement's 
%labels (tract count between region x and y or asymmetry index from 
%region y to z etc.). 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%#########################################################################
%############# SUMMARY TABLE - GRAIN: 1 row per ROI (180 rows)
%#########################################################################
ROISummary = table;

[pGender,pGenderLabel] = findgroups(T.Gender);
[pROI,pROILabel] = findgroups(T.ROILabel);


ROISummary.ROI=pROILabel;

males = T(contains(T.Gender,'Male'),:);
females = T(contains(T.Gender,'Female'),:);

perROIMale = findgroups(males.ROILabel);
perROIFemale = findgroups(females.ROILabel);

%%%%%%%%%%%%%%%   NUMTRACTS - Derived Calculations %%%%%%%%%%%%%%%
meanNumTracts_Male = splitapply(meanOmitNan,males.NumTracts,perROIMale);
ROISummary.meanNumTracts_Male = meanNumTracts_Male;

meanNumTracts_Female = splitapply(meanOmitNan,females.NumTracts,perROIFemale);
ROISummary.meanNumTracts_Female = meanNumTracts_Female;

stdNumTracts = splitapply(@std,T.NumTracts,pROI);
ROISummary.stdNumTracts = stdNumTracts;

ROISummary.EffectSize_NumTracts = (ROISummary{:,2}-ROISummary{:,3}) ./ ROISummary{:,4}

 
%%%%%%%%%%%%%%%   AGE - Derived Calculations %%%%%%%%%%%%%%%
meanAge_Male = splitapply(meanOmitNan,males.Age,perROIMale);
ROISummary.meanAge_Male = meanAge_Male;

meanAge_Female = splitapply(meanOmitNan,females.Age,perROIFemale);
ROISummary.meanAge_Female = meanAge_Female;

stdAge = splitapply(@std,T.Age,pROI);
ROISummary.stdAge = stdAge;

ROISummary.EffectSize_Age = (ROISummary{:,6}-ROISummary{:,7}) ./ ROISummary{:,8}


%#########################################################################
%############# SUMMARY TABLE - GRAIN: 1 row per ROI x ROI  = n(n-1)=(32220 rows)
%#########################################################################
ROIxROISummary = table;

[pGender,pGenderLabel] = findgroups(T.Gender);
[pROIxROI,pROILabel,pROIENDLabel] = findgroups(T.ROILabel,T.ROIENDLabel);

[x,xl,xe,xm]=findgroups(T.ROILabel,T.ROIENDLabel,T.Method);

ROIxROISummary.ROIStart=pROILabel;
ROIxROISummary.ROIEnd=pROIENDLabel;

males = T(contains(T.Gender,'Male'),:);
females = T(contains(T.Gender,'Female'),:);

perROIxROIMale = findgroups(males.ROILabel,males.ROIENDLabel);
perROIxROIFemale = findgroups(females.ROILabel,females.ROIENDLabel);

%%%%%%%%%%%%%%%   NUMTRACTS - Derived Calculations %%%%%%%%%%%%%%%
meanNumTracts_Male = splitapply(meanOmitNan,males.NumTracts,perROIxROIMale);
ROIxROISummary.meanNumTracts_Male = meanNumTracts_Male;

meanNumTracts_Female = splitapply(meanOmitNan,females.NumTracts,perROIxROIFemale);
ROIxROISummary.meanNumTracts_Female = meanNumTracts_Female;

stdNumTracts = splitapply(@std,T.NumTracts,pROIxROI);
ROIxROISummary.stdNumTracts = stdNumTracts;

ROIxROISummary.EffectSize_NumTracts = (ROIxROISummary{:,3}-ROIxROISummary{:,4}) ./ ROIxROISummary{:,5}

 
%%%%%%%%%%%%%%%   AGE - Derived Calculations %%%%%%%%%%%%%%%
meanAge_Male = splitapply(meanOmitNan,males.Age,perROIxROIMale);
ROIxROISummary.meanAge_Male = meanAge_Male;

meanAge_Female = splitapply(meanOmitNan,females.Age,perROIxROIFemale);
ROIxROISummary.meanAge_Female = meanAge_Female;

stdAge = splitapply(@std,T.Age,pROIxROI);
ROIxROISummary.stdAge = stdAge;

ROIxROISummary.EffectSize_Age = (ROIxROISummary{:,7}-ROIxROISummary{:,8}) ./ ROIxROISummary{:,9}


%#########################################################################
%############# SUMMARY TABLE - GRAIN: 1 row per ROI x ROI x Method
%#########################################################################
ROIxROIxMethodSummary = table;

[pGender,pGenderLabel] = findgroups(T.Gender);
[pROIxROIxMethod,pROILabel,pROIENDLabel,pMethod] = findgroups(T.ROILabel,T.ROIENDLabel,T.Method);

ROIxROIxMethodSummary.ROIStart=pROILabel;
ROIxROIxMethodSummary.ROIEnd=pROIENDLabel;
ROIxROIxMethodSummary.Method=pMethod;

males = T(contains(T.Gender,'Male'),:);
females = T(contains(T.Gender,'Female'),:);

perROIxROIxMethodMale = findgroups(males.ROILabel,males.ROIENDLabel,males.Method);
perROIxROIxMethodFemale = findgroups(females.ROILabel,females.ROIENDLabel,females.Method);

%%%%%%%%%%%%%%%   NUMTRACTS - Derived Calculations %%%%%%%%%%%%%%%
meanNumTracts_Male = splitapply(meanOmitNan,males.NumTracts,perROIxROIxMethodMale);
ROIxROIxMethodSummary.meanNumTracts_Male = meanNumTracts_Male;

meanNumTracts_Female = splitapply(meanOmitNan,females.NumTracts,perROIxROIxMethodFemale);
ROIxROIxMethodSummary.meanNumTracts_Female = meanNumTracts_Female;

stdNumTracts = splitapply(@std,T.NumTracts,pROIxROIxMethod);
ROIxROIxMethodSummary.stdNumTracts = stdNumTracts;

ROIxROIxMethodSummary.EffectSize_NumTracts = (ROIxROIxMethodSummary{:,4}-ROIxROIxMethodSummary{:,5}) ./ ROIxROIxMethodSummary{:,6};



%%%%%%%%%%%%%%%   AGE - Derived Calculations %%%%%%%%%%%%%%%
meanAge_Male = splitapply(meanOmitNan,males.Age,perROIxROIxMethodMale);
ROIxROIxMethodSummary.meanAge_Male = meanAge_Male;

meanAge_Female = splitapply(meanOmitNan,females.Age,perROIxROIxMethodFemale);
ROIxROIxMethodSummary.meanAge_Female = meanAge_Female;

stdAge = splitapply(@std,T.Age,pROIxROIxMethod);
ROIxROIxMethodSummary.stdAge = stdAge;

ROIxROIxMethodSummary.EffectSize_Age = (ROIxROIxMethodSummary{:,8}-ROIxROIxMethodSummary{:,9}) ./ ROIxROIxMethodSummary{:,10};



%%%%%%%%%%%%%%%   TractsToRender - Derived Calculations %%%%%%%%%%%%%%%
meanTractsToRender_Male = splitapply(meanOmitNan,males.TractsToRender,perROIxROIxMethodMale);
ROIxROIxMethodSummary.meanTractsToRender_Male = meanTractsToRender_Male;

meanTractsToRender_Female = splitapply(meanOmitNan,females.TractsToRender,perROIxROIxMethodFemale);
ROIxROIxMethodSummary.meanTractsToRender_Female = meanTractsToRender_Female;

stdTractsToRender = splitapply(@std,T.TractsToRender,pROIxROIxMethod);
ROIxROIxMethodSummary.stdTractsToRender = stdTractsToRender;

ROIxROIxMethodSummary.EffectSize_TractsToRender = (ROIxROIxMethodSummary{:,8}-ROIxROIxMethodSummary{:,9}) ./ ROIxROIxMethodSummary{:,10};



%scatter(rostral.Age,rostral.NumTracts)
%########################
%
% BEAST
%
%########################
for i =1:height(ROIxROIxMethodSummary)
    Row = ROIxROIxMethodSummary(i,:);
       
    out=T(ismember(T.ROILabel,Row.ROIStart) & ismember(T.ROIENDLabel,Row.ROIEnd) & ismember(T.Method,Row.Method),:);
    %corr(out.Age,out.NumTracts);
    ROIxROIxMethodSummary.Correlation_Age_NumTracts(i) = corr(out.Age,out.NumTracts);
    ROIxROIxMethodSummary.Correlation_Age_TractsToRender(i) = corr(out.Age,out.TractsToRender);
    %[R,P] = corrcoef(___)
    %[R,P,RL,RU] = corrcoef(___)
    %[R,P] = corrcoef(out.Age,out.NumTracts);
    
end
%########################
%
% END OF BEAST
%
%########################
%{'ctx-lh-inferiorparietal','ctx-lh-parstriangularis','roi'}
out=T(ismember(T.ROILabel,'ctx-lh-inferiorparietal') & ismember(T.ROIENDLabel,'ctx-lh-parstriangularis') & ismember(T.Method,'roi'),:);
scatter(out.Age,out.NumTracts)
scatter(out.Age,out.TractsToRender)
scatter(out.Age,out.LinesToRender)
scatter(out.Age,out.meanFA)
scatter(out.Age,out.meanADC)
scatter(out.Age,out.TractsToRender_asymidx)
corr(out.Age,out.TractsToRender_asymidx)


fcnCorrMatrixPlot(out,['Age','NumTracts','TractsToRender'])

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Assymmetry
%wm_lh_pericalcarine=T(contains(T.ROILabel,'wm-lh-pericalcarine'),:);
%gscatter(wm_lh_pericalcarine.LinesToRender,wm_lh_pericalcarine.Age,wm_lh_pericalcarine.Gender)
%keywordsStart=["wm-lh-rostralanteriorcingulate","wm-rh-rostralanteriorcingulate"];
keywordsStart=["wm-rh-rostralanteriorcingulate"];
rostral=T(contains(T.ROILabel,keywordsStart),:);
keywordsEnd=["wm-rh-frontalpole"];%,'wm-lh-frontalpole'];
rostralToFrontalPole = rostral(contains(rostral.ROIENDLabel,keywordsEnd),:);
%[rostralGroups,rostralGenderNames,LeftOrRightNames]=findgroups(rostral.Gender,rostral.LeftOrRight);
[rostralGroups,rostralGenderNames,LeftOrRightNames]=findgroups(rostralToFrontalPole.Gender,rostralToFrontalPole.LeftOrRight);
%gscatter(rostral.Age,rostral.meanFA,rostralGroups);
legendTitles=strcat(rostralGenderNames," ",LeftOrRightNames)
gscatter(rostralToFrontalPole.Age,rostralToFrontalPole.meanFA,rostralGroups,'rkgb','o*',8,'on','Age','meanFA');


%FIG3
%Assymmetry

keywordsStart=["wm-lh-medialorbitofrontal","wm-rh-medialorbitofrontal"];
rostral=T(contains(T.ROILabel,keywordsStart),:);
keywordsEnd=["wm-lh-rostralanteriorcingulate","wm-rh-rostralanteriorcingulate"];%,'wm-lh-frontalpole'];
rostralToFrontalPole = rostral(contains(rostral.ROIENDLabel,keywordsEnd),:);
%[rostralGroups,rostralGenderNames,LeftOrRightNames]=findgroups(rostral.Gender,rostral.LeftOrRight);
[rostralGroups,rostralGenderNames,LeftOrRightNames]=findgroups(rostralToFrontalPole.Gender,rostralToFrontalPole.LeftOrRight);
%gscatter(rostral.Age,rostral.meanFA,rostralGroups);
legendTitles=strcat(rostralGenderNames," ",LeftOrRightNames)
gscatter(rostralToFrontalPole.Age,rostralToFrontalPole.meanFA,rostralGroups,'rkgb','o*',8,'on','Age','meanFA-asymidx');



