# Dołączanie potrzebnych bibliotek

# install.packages("ggplot2")
# install.packages("GGally")
# install.packages("cluster")
# install.packages("magrittr")

library(ggplot2)
library(GGally)
library(cluster) 
library(magrittr)

# Zadanie 1:
my_list <- 1:10
my_list %<>% log2() %>% sin() %>% sum() %>% sqrt()
print(my_list)

data(iris)
print(head(iris))

result_1_5 <- iris %>% aggregate(. ~ Species, ., mean)
print(result_1_5)

# Zadanie 2:
p1 <- ggplot(iris, aes(x = Petal.Width, color = Species)) +
    geom_histogram(fill="white", position="dodge", bins=20) +
    geom_vline(data=result_1_5, aes(xintercept=Petal.Width, color=Species), linetype='dashed') +
    labs(x='Rodzaj irysa', y='Szerokość płatka', title='Dane dotyczące irysów')
ggsave("./wykres_1.jpg", plot = p1)

p2 <- ggpairs(iris, aes(color = Species))
ggsave("./wykres_2.jpg", plot = p2)

# Zadanie 3:
x <- iris[,1:4]
y <- iris[,5]
result_lst <- c()

for (i in 1:10) {
    kmeans_rslt <- kmeans(x, i)
    result_lst <- append(result_lst, kmeans_rslt$tot.withinss)
}

p3 <- ggplot(data.frame(iteration = 1:length(result_lst), value = result_lst), 
    aes(x = iteration, y = result_lst)) + geom_line()
ggsave("./wykres_3.jpg", plot = p3)

kmeans_rslt = kmeans_rslt(x, 3)
p4 <- ggplot(iris, aes(x = Sepal.Width, y = Petal.Width, color = kmeans_rslt$cluster)) + geom_point()
ggsave("./wykres_4.jpg", plot = p4)

p5 <- ggplot(iris, aes(x = Sepal.Width, y = Petal.Width, color = Species)) + geom_point()
ggsave("./wykres_5.jpg", plot = p5)