# Mission 1 : Affiche les 10 premières lignes du dataset
imdb <-read.csv("http://bit.ly/imdbratings")
head(imdb,10)


# Mission 2 : Trie ton dataframe en ordre croissant par rapport à la colonne star_rating
imdb_star <- imdb[order(imdb$star_rating),]



# Mission 3 : Répond au questions ci-dessous :
# Quel est le start-rating médian ?
median(imdb$star_rating)


# Quel est le genre le mieux noté ?
library(dplyr)
imdb %>% group_by(genre) %>% summarise (avg = mean(star_rating))

# Quel est le pourcentage d'apparition de chaque genre de film ?
cnt <- count(imdb, vars = imdb$genre)
(cnt / length(imdb$genre))*100

# Mission 4 : Affiche les films qui ont une durée supérieure à 200 pour le genre est Drama, Comedy ou Action
over9000 <- function(genra){
  temp_genre <- imdb %>% filter(imdb$genre == genra)
  over200 <- temp_genre %>% filter(temp_genre$duration >= 200)
  return(over200)
}

over9000("Drama")
over9000("Comedy")
over9000("Action")
