# Mission 1 : Afficher le message "Bonjour R". Vous devez utiliser une variable str que vous passerez en paramètre de cat
a = "Bonjour R"
a

# Mission 2 : Créer une fonction qui prend en paramètre 2 nombres, et indique s'ils sont égaux ou pas.
égaux <- function(nombre1, nombre2){
  if (nombre1 == nombre2){return(print("Les nombres sont égaux")) }}
égaux(2,2)


# Mission 3 : Créer une fonction qui prend en paramètre un nombre correspondant au salaire brut et renvoie le net pour les cadres.
salaire<-function(salaireBrut){
  salaireNet<-salaireBrut*0.75
  return(salaireNet)}
salaire(2000)


# Mission 4 : Créer une fonction qui prend en paramètre un jour, et renvoie le jour suivant (pour dimanche il renvoie lundi). 
jours <-c("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
day<-function(jour){
  jour_l <- c(jour)
  for(i in 1:length(jours)){
    if (jour_l[[1]] == "sunday"){print("monday")}
    else if (jour_l[1]==jours[i]){print(jours[i+1])}}}
day("tuesday")

1:length(jours)

# Mission 5 : Cré une fonction qui compte le nombre de lettre en commun qu'on 2 chaines de caractères
chaine1 <- c("y","j","r","k","m")
chaine2 <- c("a","v","r","l","s")

compare<-function(chaine1,chaine2){charmatch(chaine1,chaine2)
  
}
compare(chaine1, chaine2)
