seaflow_data <- read.csv(file="seaflow_21min.csv", header=TRUE, sep=",")
seaflow_data <- seaflow_data[1:72342,]

print("============================================================\n")
print("Q2 answer: summary of seaflow data, pop")
print(summary(seaflow_data$pop))
print("============================================================\n")
print("Q3 answer: summary of fsc_small")
print(summary(seaflow_data$fsc_small))

library(caret)
dataPart <-createDataPartition(seaflow_data$cell_id,p=0.5,list=FALSE)
training <- seaflow_data[-dataPart,]
testset<-seaflow_data[dataPart,]

print("============================================================\n")
print("Q4 answer: mean of the time column in training set")
print(mean(training$time))

library(ggplot2)

#ggplot(seaflow_data, aes(x=seaflow_data$pe,y=seaflow_data$chl_small,color=seaflow_data$pop))+geom_point(size=2)

print("============================================================\n")
print("Q5 answer: check the plot to tell which mixes with 'ultra'")
print(ggplot(seaflow_data, aes(x=pe,y=chl_small,color=pop))+geom_point(size=2))

library(rpart)

fol <-formula(pop~fsc_small+fsc_perp+fsc_big+pe+chl_big+chl_small)

rpartmodel <-rpart(fol, method = "class", data=training)

print("============================================================\n")
print("Q6 answer: decision tree model, check for what class is not present in the tree")
print("Q7 answer: decision tree model, check threshold for pe on which split happens")
print("Q8 answer: decision tree model, check for what features are used for comparison most")
print(rpartmodel)

#rpartmodelVars <- names(rpartmodel[,1:13])

dtpredict <- predict(rpartmodel, data=testset)

# get the dtprediction for each entry
i1 <- max.col(dtpredict, ties.method="first")
dtpredictresult <- data.frame(cell_id=rownames(dtpredict), pop=colnames(dtpredict)[i1])

validationdata <- testset[, c("cell_id", "pop")]

# since the levels of both validation and predictions are not same (remember crypto
# cannot be predicted by the rpart model?) we need to fix that. 
# first we extract the predicted pop values:
dttest <- dtpredictresult$pop
# next we extract the pop values in the validation/test data
valtest <- validationdata$pop 
# now fix the levels:
dttest <-factor(dttest, levels=levels(valtest))

evaluaterpartpredict <- dttest==valtest
accuracyrpartpredict <- sum(evaluaterpartpredict)/length(valtest)

print("============================================================\n")
print("Q9 answer: accuracy of the rpart predict")
print(accuracyrpartpredict)

library(randomForest)

randomforestmodel <- randomForest(fol, data=training)
randforestpredict <- predict(randomforestmodel, data=testset)
rftest <- randforestpredict == valtest
accuracyrandforestpredict <- sum(rftest)/length(valtest)

print("============================================================\n")
print("Q10 answer: accuracy of the random forest predict")
print(accuracyrandforestpredict)

print("============================================================\n")
print("Q11 answer: see which values have highest Gini score")
print(importance(randomforestmodel))

library(e1071)
svmmodel <- svm(fol, data=training)
svmpredict <- predict(svmmodel, data=testtet)
svmtest <- svmpredict == valtest
accuracysvm <- sum(svmtest)/length(valtest)

print("============================================================\n")
print("Q12 answer:  accuracy of the svm predict")
print(accuracysvm)

# for the next creating a table, we have one of the set (predicted/training) less number
# of rows than the test, so we just add a dummy null set in the prediction to get the table working
randforestpredict[36172] <- "null"
svmpredict[36172] <- "null"

print("============================================================\n")
print("Q13 answer: confusing matrix for random forest prediction")
print(table (pred=randforestpredict, true=testset$pop))
print("Q13 answer: confusing matrix for svm prediction")
print(table (pred=svmpredict, true=testset$pop))

print("============================================================\n")
print("Q15 answer: to answer this, plot all measurements against time, see which is not continuous")
print(ggplot(training, aes(x=time,y=fsc_small,color=pop))+geom_point(size=1))
print(ggplot(training, aes(x=time,y=fsc_perp,color=pop))+geom_point(size=1))
# this next one!
print(ggplot(training, aes(x=time,y=fsc_big,color=pop))+geom_point(size=1))
print(ggplot(training, aes(x=time,y=pe,color=pop))+geom_point(size=1))
print(ggplot(training, aes(x=time,y=chl_small,color=pop))+geom_point(size=1))
print(ggplot(training, aes(x=time,y=chl_big,color=pop))+geom_point(size=1))

# remove data pertaining to file 208
training_minus208 <- subset(training, training[,c("file_id")] != 208) 
testset_minus208 <- subset(testset, testset[, c("file_id")] != 208)

svmmodel2 <- svm(fol, data=training_minus208)
svmpredict2 <- predict(svmmodel, data=testset_minus208)
validationdata2 <- testset_minus208[, c("cell_id", "pop")]
valtest2 <- validationdata2$pop 
svmtest2 <- svmpredict2 == valtest2
accuracysvm2 <- sum(svmtest2)/length(valtest2)

print("============================================================\n")
print("Q14 answer:  accuracy of the svm predict after cleaning data")
print(accuracysvm2)

