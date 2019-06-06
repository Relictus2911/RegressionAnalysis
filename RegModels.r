#! Rscript
pub <- read.table("main.tsv", header=TRUE)
print(cor(pub))
plot(pub,col=rgb(0,100,0,50,maxColorValue=255))

regmodel <- lm(likes~., data = pub) #first model
print(summary(regmodel))
regmodel <- lm(likes~ coms + favs, data = pub) #first model
#print(summary(regmodel))
regmodel2 <- lm(likes~ coms*favs*size, data = pub) #second model
print(summary(regmodel2))
regmodel3 <- lm(likes~ poly(coms,2)+poly(favs,2)+poly(size,2), data = pub) #third model
print(summary(regmodel3))


plot(regmodel)
plot(regmodel2)
plot(regmodel3)