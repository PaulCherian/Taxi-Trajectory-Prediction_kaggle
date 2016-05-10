library(grid)
library(MASS)
library(neuralnet)

# reading the dataset
dataset <- read.csv('input_train1.csv', header=T)
df <- dataset

# defining the normalizing function
normalize <- function(x){return((x-min(x))/(max(x)-min(x)))}

# normalizing the dataset
df_norm <- as.data.frame(lapply(df,normalize))

# creating a training and a testing set for cross validation
df_shuff <- df_norm[order(runif(100000)),]
df_train <- df_shuff[1:75000,]
df_test <- df_shuff[75001:100000,]

# names of the columns
n <- names(df_train)
f <- as.formula(paste("Destination_grid ~", paste(n[!n %in% "Destination_grid"], collapse = " + ")))
n1 <- neuralnet(f, data = df_train, hidden=1)
plot(n1)

p1 <- compute(n1,df_test[,-c(3)])
predictions1 <- p1$net.result
names(predictions1) <- "Destination"

# calculating the rmse value
sqrt(mean((df_test$Destination_grid - predictions1)^2))

# 2nd iteration
# reading the dataset
dataset <- read.csv('input_train2.csv', header=T)
df <- dataset

# defining the normalizing function
normalize <- function(x){return((x-min(x))/(max(x)-min(x)))}

# normalizing the dataset
df_norm <- as.data.frame(lapply(df,normalize))

# creating a training and a testing set for cross validation
df_shuff <- df_norm[order(runif(100000)),]
df_train <- df_shuff[1:75000,]
df_test <- df_shuff[75001:100000,]

# names of the columns
n <- names(df_train)
f <- as.formula(paste("Destination_grid ~", paste(n[!n %in% "Destination_grid"], collapse = " + ")))
n1 <- neuralnet(f, data = df_train, hidden=1)
plot(n1)

p1 <- compute(n1,df_test[,-c(3)])
predictions1 <- p1$net.result
names(predictions1) <- "Destination"

# calculating the rmse value
sqrt(mean((df_test$Destination_grid - predictions1)^2))

