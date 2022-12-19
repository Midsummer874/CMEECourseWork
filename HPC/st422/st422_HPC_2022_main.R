
# If you opt to write everything yourself from scratch please ensure you use
# EXACTLY the same function and parameter names and beware that you may lose
# marks if it doesn't work properly because of not using the pro-forma.

# name <- "Shengge Tong"
# preferred_name <- "TSG"
# email <- "shengge.tong22@imperial.ac.uk"
# username <- "st422"

# Please remember *not* to clear the workspace here, or anywhere in this file.
# If you do, it'll wipe out your username information that you entered just
# above, and when you use this file as a 'toolbox' as intended it'll also wipe
# away everything you're doing outside of the toolbox.  For example, it would
# wipe away any automarking code that may be running and that would be annoying!

# Question 1
species_richness <- function(community){
  length(unique(community))
}

# Question 2
init_community_max <- function(size){
  seq(1, size, by=1)
}

# Question 3
init_community_min <- function(size){
  rep(size, size)
}

# Question 4
choose_two <- function(max_value){
  sample(c(1:max_value), 2, replace=F)
}

# Question 5 Randomly replacing an existing population with a
neutral_step <- function(community){
  indices <- choose_two(length(community))
  community[indices[1]] <- community[indices[2]]
  return(community)
}

# Question 6
neutral_generation <- function(community){
  steps <- length(community)/2
  steps <- sample(c(ceiling(steps), floor(steps)), 1)

  for (i in 1:steps) {
    community <- neutral_step(community)
  }
  return(community)
}

# Question 7
neutral_time_series <- function(community,duration)  {
  result <- rep(1:duration+1)
  result[1] <- species_richness(community)
  
  for (i in 2:duration+1) {
    community <- neutral_generation(community)
    result[i] <- species_richness(community)
  }
  return(result)
}


# Question 8
question_8 <- function() {
  

  png(filename="question_8.png", width = 600, height = 400)
  # plot your graph here
  y <- neutral_time_series(community = init_community_max(100), duration = 200)
  x <- c(1:201)
  plot(x, y, main = "Question_8: Richness for 100 individuals and 200 generations",
       xlab="neutral_generations", ylab="species_richness")
  Sys.sleep(0.1)
  dev.off()
  
  return("This richness will converge to 1, because the total number of individuals is too small, and also smaller than the durations, and each iteration is too fast, resulting in a rapidly decreasing species size.")
}

# Question 9
neutral_step_speciation <- function(community,speciation_rate)  {
  s = sample(c("new","old"),size=1, prob=c(speciation_rate,1-speciation_rate))
  if (s == "new") {
    new = max(community) + 1 # new species
    index = sample(c(1:length(community)), 1, replace=F) # random index
    community[index] <- new
    community
  }else{
    neutral_step(community)
  }
  
}

# Question 10
neutral_generation_speciation <- function(community,speciation_rate)  {
  steps <- length(community)/2
  steps <- sample(c(ceiling(steps), floor(steps)), 1)
  
  for (i in 1:steps) {
    community <- neutral_step_speciation(community, speciation_rate)
  }
  community
}

# Question 11
neutral_time_series_speciation <- function(community,speciation_rate,duration)  {
  result <- rep(1:duration+1)
  result[1] <- species_richness(community)
  
  for (i in 2:duration+1) {
    community <- neutral_generation_speciation(community, speciation_rate)
    result[i] <- species_richness(community)
  }
  
  result
}

# Question 12
question_12 <- function()  {

  png(filename="question_12.png", width = 600, height = 400)
  # plot your graph here
  y_max <- neutral_time_series_speciation(community = init_community_max(100), speciation_rate=0.1, duration = 200)
  y_min <- neutral_time_series_speciation(community = init_community_min(100), speciation_rate=0.1, duration = 200)
  
  x <- c(1:201)
  plot(x, y_max, main = "Question_9: neutral_time_series_speciation with max(red) and min(blue) 100", col="red", 
       xlab="neutral_generations", ylab="species_richness")
  lines(x, y_min, col="blue")
  
  Sys.sleep(0.1)
  dev.off()
  
  return("For init_community_min, the species richness is increasing over time. For init_community_max,
         the species richness decreases over time. However, they will both eventually converge to the same level.")
}

# Question 13
species_abundance <- function(community)  {
  tab <- table(community)
  as.vector(tab[order(tab,decreasing = TRUE)])
}

# Question 14
octaves <- function(abundance_vector) {
  # Divide the interval first
  max_a <- max(abundance_vector)
  max_n <- floor(log2(max_a)) + 1
  
  results <- rep(0, max_n)
  
  for (val in abundance_vector) {
    for (i in 1:max_n) {
      h = 2**i
      l = 2**(i-1)
      if ((val < h) & (val >= l)){
        results[i] <- results[i]+1
        break
      }
    }
  }
  results
  
}

# Question 15
sum_vect <- function(x, y) {
  len <- length(x) - length(y)
  if (len > 0){
    for (i in 1:len){
      y <- append(y, 0)
    }
  }
  if (len <0){
    for (i in 1:abs(len)){
      x <- append(x, 0)
    }
  }
  return (x+y)
}

# Question 16 
question_16 <- function() {
  png(filename="question_16_min.png", width = 600, height = 400)
  # plot your graph here
  t_tmp <- neutral_time_series_speciation(community = init_community_min(100), speciation_rate=0.1, duration = 200)
  oct0 = octaves(species_abundance(t_tmp))
  # start a further 2000 generations , record every 20 generations
  octaves_list <- c(mean(oct0))
  for (i in 1:2000){
    t_tmp <- neutral_time_series_speciation(community = t_tmp, speciation_rate=0.1, duration = 1)
    if (i%%20 == 0){
      oct_tmp = octaves(species_abundance(t_tmp))
      octaves_list <- append(octaves_list, mean(oct_tmp))
    }
  }
  barplot(octaves_list)
  Sys.sleep(0.1)
  dev.off()
  
  
  png(filename="question_16_max.png", width = 600, height = 400)
  # plot your graph here
  t_tmp <- neutral_time_series_speciation(community = init_community_max(100), speciation_rate=0.1, duration = 200)
  oct0 = octaves(species_abundance(t_tmp))
  # start a further 2000 generations , record every 20 generations
  octaves_list <- c(mean(oct0))
  for (i in 1:2000){
    t_tmp <- neutral_time_series_speciation(community = t_tmp, speciation_rate=0.1, duration = 1)
    if (i%%20 == 0){
      oct_tmp = octaves(species_abundance(t_tmp))
      octaves_list <- append(octaves_list, mean(oct_tmp))
    }
  }
  barplot(octaves_list)
  Sys.sleep(0.1)
  dev.off()
  
  return("The results of both graphs show that, independent of the initial population size, 
         as we iterate enough, the population size will gradually decrease to a very low level, 
         so that the average of the species abundance octave vector will also be very low and 
         converge to the almost same level.")
}

# Question 17
neutral_cluster_run <- function(speciation_rate, size, wall_time, interval_rich, interval_oct, burn_in_generations, output_file_name) {
    community  <- init_community_min(size)
    wall_time <- wall_time*60  #  in seconds
    interval_rich_index <- 1
    burn_in_index <- 1
    time_series <- c()
    abundance_list <- list()
    interval_oct_index <- 1
    
    ptm <- proc.time()
    while (TRUE){
      interval_rich_index <- interval_rich_index + 1
      burn_in_index <- burn_in_index + 1
      interval_oct_index <- interval_oct_index + 1
        
      community <- neutral_generation_speciation(community = community, speciation_rate=speciation_rate)

      
      if ((interval_rich_index%%interval_rich==0) & (burn_in_index<burn_in_generations)){
         sr <- species_richness(community)
         time_series <- append(time_series, sr)
      }
      
      if (interval_oct_index%%interval_oct){
        oct_tmp = octaves(species_abundance(community))
        abundance_list <- append(abundance_list, oct_tmp)
      }
      
      totalSec <- proc.time() - ptm
      totalSec <-getElement(totalSec, "elapsed")
      
      if (totalSec >= wall_time){
        break
      }
    }
    
    #save to rda file
    save(time_series, abundance_list, community, file = output_file_name)
  
}

# Questions 18 and 19 involve writing code elsewhere to run your simulations on
# the cluster

# Question 20 
process_neutral_cluster_results <- function() {
  
  
  combined_results <- list() #create your list output here to return
  # save results to an .rda file
  
}

plot_neutral_cluster_results <- function(){

    # load combined_results from your rda file
  
  
  
    png(filename="plot_neutral_cluster_results.png", width = 600, height = 400)
    # plot your graph here
    Sys.sleep(0.1)
    dev.off()
    
    return(combined_results)
}


# Question 21
state_initialise_adult <- function(num_stages,initial_size){
  state <- rep(0, num_stages)
  state[num_stages] <- initial_size
  return(state)
}

# Question 22
state_initialise_spread <- function(num_stages,initial_size){
  
  state <- rep(floor(initial_size/num_stages), num_stages)
  
  remaining <- initial_size - floor(initial_size/num_stages)*num_stages
  
  while(TRUE){

    for (i in 1:num_stages){
      if (remaining ==0){
        break
      }
      state[i] <- state[i] + 1
      remaining <- remaining - 1
    }
    
    if (remaining ==0){
      break
    }
    
  }
  
  return(state)
}

# Question 23
deterministic_step <- function(state,projection_matrix){
  return(projection_matrix%*%state)
}

# Question 24
deterministic_simulation <- function(initial_state,projection_matrix,simulation_length){
  population_size <- c(sum(initial_state))
  new_state <- initial_state
  for (i in 1:simulation_length){
    new_state <- deterministic_step(new_state, projection_matrix)
    population_size <- append(population_size, sum(new_state))
  }
  return(population_size)
}

# Question 25
question_25 <- function(){
  
  png(filename="question_25.png", width = 600, height = 400)
  # plot your graph here
  projection_matrix <- matrix(c(0.1, 0.6, 0.0, 0.0,
                                0.0, 0.4, 0.4, 0.0,
                                0.0, 0.0, 0.7, 0.25,
                                2.6, 0.0, 0.0, 0.4),nrow=4,ncol=4)

  
  adult_state <- state_initialise_adult(4, 100)
  even_state <- state_initialise_spread(4,100)
  a <- deterministic_simulation(adult_state, projection_matrix, 24)
  e <- deterministic_simulation(even_state, projection_matrix, 24)

  x <- c(1:length(a))
  plot(x, a, main = "Question_25 popluation size for two different initial state (adult state: red)", col="red", 
       xlab="simulation", ylab="popluation_size")
  lines(x, e, col="blue")
  
  Sys.sleep(0.1)
  dev.off()
  
  return("The adult state drops a little at the beginning, but then increases rapidly.
         In the case of the evenly state, the growth is always rapid. At the same time, 
         the adult state is growing faster and more rapidly.")
}

# Question 26
trinomial <- function(pool,probs) {
  if (probs[1] == 1){ # special case
    return(c(pool,0,0))
  }
  
  fristEventInd <- rbinom(1, pool, probs[1]) # first event. no. individuals
  remaining_pool = pool - fristEventInd
  
  prob_event_2 <- probs[2]/(1-probs[1])
  secondEventInd <-rbinom(1, remaining_pool, prob_event_2)
  thirdEventInd <- remaining_pool - secondEventInd
  return(c(fristEventInd, secondEventInd, thirdEventInd))

}

# Question 27
survival_maturation <- function(state,projection_matrix) {
  #print(state)
  new_state <- rep(0, length(state))
  for (i in 1:(length(state)-1)){
    #pprint(paste(c("stage", i), collapse = " "))
    inds <- state[i]
    
    probs <- rep(0, length(state))
    
    probs <- projection_matrix[i:length(state),i]
    
    #pprint(paste(c("probs", probs), collapse = " "))
    
    change_vec <-trinomial(inds, probs) 
    #pprint(paste(c("change_vec ", change_vec), collapse = " "))
    stay <- change_vec[1]
    mature <-change_vec[2]

    new_state[i] <- new_state[i] + stay # stay 
    new_state[i+1] <- mature# mautrition 
      
  

    #pprint(new_state)
  }
  #pprint("final")
  probs <- c(projection_matrix[length(state), length(state)])
  probs <- append(probs, rep(0, length(state)-1))
  #pprint(probs)
  change_vec <-trinomial(state[length(state)], probs)
  #pprint(change_vec)
  new_state[length(new_state)] <- new_state[length(new_state)] + change_vec[1]
  #pprint(new_state)
  return(new_state)
}

# Question 28
random_draw <- function(probability_distribution) {
  sample <- runif(1, 0, 1)
  
  cumulative_distribution <- cumsum(probability_distribution)
  
  value <- min(which(cumulative_distribution >= sample))
  
  # Return the value.
  return(value)
}

# Question 29
stochastic_recruitment <- function(projection_matrix,clutch_distribution){
  
  recruitment_rate <- projection_matrix[1, ncol(projection_matrix)]
  expected_clutch_size <- 0
  for (i in 1:length(clutch_distribution)){
    expected_clutch_size <- expected_clutch_size + i*clutch_distribution[i]
  }
  
  return(recruitment_rate / expected_clutch_size)
  
}

# Question 30
offspring_calc <- function(state,clutch_distribution,recruitment_probability){
  #print(recruitment_probability)
  adults <- state[3]
  
  #  draw the number of individuals which recruit:
  clutches <- rbinom(1, adults, recruitment_probability)
  
  total_offspring <- 0
  
  if (clutches > 0) {
    for (i in 1:length(clutches)){
      clutch_sizes <- random_draw(clutch_distribution)
      total_offspring <- total_offspring + clutch_sizes
    }

  }
  
  return(total_offspring)
}

# Question 31
stochastic_step <- function(state,projection_matrix,clutch_distribution,recruitment_probability){
  #Apply survival and maturation to generate new_state
  new_state <- survival_maturation(state, projection_matrix)

    #Compute the number of offspring produced by state and add to new_state
  offspring <- offspring_calc(state, clutch_distribution, recruitment_probability)
  #print(paste(c("offspring", offspring), collapse = " "))
  new_state[1] <- new_state[1] + offspring

  return(new_state)
}


# Question 32
stochastic_simulation <- function(initial_state,projection_matrix,clutch_distribution,simulation_length){
  population_size <- c(sum(initial_state))
  new_state <- initial_state
  for (i in 1:simulation_length){
    if (sum(new_state) == 0) {
      population_size <- append(population_size, rep(0, simulation_length - i + 1))
      break
    }
    recruitment_prob <- stochastic_recruitment(projection_matrix, clutch_distribution)
    new_state <- stochastic_step(new_state, projection_matrix, clutch_distribution, recruitment_prob)
    population_size <- append(population_size, sum(new_state))
  }
  return(population_size)
}

# Question 33
question_33 <- function(){
  clutch_distribution <- c(0.06,0.08,0.13,0.15,0.16,0.18,0.15,0.06,0.03)
  png(filename="question_33.png", width = 600, height = 400)
  # plot your graph here
  projection_matrix <- matrix(c(0.1, 0.6, 0.0, 0.0,
                                0.0, 0.4, 0.4, 0.0,
                                0.0, 0.0, 0.7, 0.25,
                                2.6, 0.0, 0.0, 0.4),nrow=4,ncol=4)
  
  
  adult_state <- state_initialise_adult(4, 24)

  a <- stochastic_simulation(adult_state,projection_matrix,clutch_distribution,24)
  even_state <- state_initialise_spread(4, 24)
  e <- stochastic_simulation(even_state,projection_matrix,clutch_distribution,24)
  
  x <- c(1:length(a))
  plot(x, a, main = "Question_33 stochastic_simulations: adult state(red) vs evenly state(blue)", col="red", 
       xlab="simulation", ylab="popluation_size")
  lines(x, e, col="blue")
  

  Sys.sleep(0.1)
  dev.off()
  
  return("deterministic is based on averages and stochastic simulations is random. random means no pattern.")
}

# Questions 34 and 35 involve writing code elsewhere to run your simulations on the cluster

# Question 36
question_36 <- function(){
  
  png(filename="question_36.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()
  
  return("type your written answer here")
}

# Question 37
question_37 <- function(){
  
  png(filename="question_37_small.png", width = 600, height = 400)
  # plot your graph for the small initial population size here
  Sys.sleep(0.1)
  dev.off()
  
  png(filename="question_37_large.png", width = 600, height = 400)
  # plot your graph for the large initial population size here
  Sys.sleep(0.1)
  dev.off()
  
  return("type your written answer here")
}



# Challenge questions - these are optional, substantially harder, and a maximum
# of 14% is available for doing them. 

# Challenge question A
Challenge_A <- function() {
  
  
  
  png(filename="Challenge_A_min.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()
  
  png(filename="Challenge_A_max.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()

}

# Challenge question B
Challenge_B <- function() {
  
  
  
  png(filename="Challenge_B.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()

}

# Challenge question C
Challenge_C <- function() {
  
  
  
  png(filename="Challenge_C.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()

}

# Challenge question D
Challenge_D <- function() {
  
  
  
  png(filename="Challenge_D.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()
  
  return("type your written answer here")
}

# Challenge question E
Challenge_E <- function(){
  
  
  
  png(filename="Challenge_E.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()
  
  return("type your written answer here")
}

# Challenge question F
Challenge_F <- function(){
  
  
  
  png(filename="Challenge_F.png", width = 600, height = 400)
  # plot your graph here
  Sys.sleep(0.1)
  dev.off()
  
}
