pokemon <-read.csv("https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv")
View(pokemon)
install.packages("ggplot2")
library(ggplot2)

# geom_line()
# geom_point()
# geom_dotplot()
# geom_histogram()
# geom_bar()
# geom_boxplot()
# coord_polar()


#geom_line
ggplot(pokemon, aes(x=pokemon$X., y = pokemon$Total[order(Total)]))+geom_line()


#Geom_point
ggplot(pokemon, aes(x = pokemon$Attack, y = pokemon$Sp..Atk))+geom_point(aes(size = pokemon$Speed))
#Geom_point with a flex
ggplot(pokemon, aes(x = pokemon$Attack, y = pokemon$Sp..Atk))+
geom_point(aes(size = pokemon$Speed))+geom_text(label=pokemon$Name)

#Geom_dotplot
ggplot(pokemon, aes(x = pokemon$Attack, y = pokemon$Sp..Atk)) +geom_dotplot(binaxis='y', stackdir='center')

# geom_histogram()
ggplot(pokemon, aes(x = pokemon$Attack)) +geom_histogram()

#geom_bar
ggplot(pokemon, aes(x=pokemon$Attack))+geom_bar()

#geom_boxplot
ggplot(pokemon, aes(x=as.factor(pokemon$Generation), y=pokemon$Attack))+geom_boxplot()

#coord_polar
test <- ggplot(pokemon,aes(factor(pokemon$Generation)))+geom_bar()
test + coord_polar()
