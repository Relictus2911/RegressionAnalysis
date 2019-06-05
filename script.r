#! Rscript
pub <- read.table("result.tsv", header=TRUE)
print(cor(pub))
df <- data.frame(pub)
regmodel <- lm(likes~., data = pub)
print(summary(regmodel))
regmodel2 <- lm(likes~ coms*favs*size, data = pub)
print(summary(regmodel2))
regmodel3 <- lm(likes~ poly(coms,2)+poly(favs,2)+poly(size,2), data = pub)
print(summary(regmodel3))


#boxplot(hist)
#hist(df$likes)
#plot(hist,col=rgb(0,100,0,50,maxColorValue=255))
#plot(regmodel)
#scatter.smooth(hist)

print(anova(regmodel, regmodel2))