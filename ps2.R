

## compute the clustering coefficient and mean geodesic path lengths
# library(igraph)

# # Read the edge list as an undirected graph
# g <- read_graph("Berkeley13.txt", format = "edgelist", directed = FALSE)

# m <- gsize(g) # 1704888 edges
# a <- log10(m) # 6.2
# cat("Number of edges: ", m, "\n")
# cat("log10(m): ", a, "\n")
# # r <- c(1:8)
# r <- 9:12
# r_star <- 20 * m

# # write column header
# write("r\tC\tl_mu", "ps2_q3_log_step.tsv", append=TRUE)

# # compute original clustering coef and mean geodes
# C <- transitivity(g, type = "global")
# l_mu <-  mean_distance(g, directed = FALSE, unconnected = TRUE, weights = NA)
# # first row
# write(paste0(0, "\t", C, "\t", l_mu), "ps2_q3_log_step.tsv",append=TRUE)

# # do for r_star
# g_r <- g
# rewires <- r_star
# g_r <- rewire(g_r, keeping_degseq(niter=rewires))
# C <- transitivity(g_r, type = "global")
# l_mu <-  mean_distance(g_r, directed = FALSE, unconnected = TRUE, weights = NA)
# write(paste0(r_star, "\t", C, "\t", l_mu), "ps2_q3_log_step.tsv",append=TRUE)


# # rewire the graph and compute the clustering coef and mean geodes
# g_r <- g
# for (r_i in r)
# {
#     rewires <- 10^r_i 
#     cat("Iteration: ", r_i, "rewires: ", rewires, "\n")
#     g_r <- rewire(g_r, keeping_degseq(niter=rewires))
#     C <- transitivity(g_r, type = "global")
#     cat("Clustering coef: ", C, "\n")
#     l_mu <-  mean_distance(g_r, directed = FALSE, unconnected = TRUE, weights = NA)
#     cat("Mean geodesic path length: ", l_mu, "\n")
#     write(paste0(rewires, "\t", C, "\t", l_mu), "ps2_q3_log_step.tsv",append=TRUE)
# }
# quit()

### plot rewire versus C and <l>
library(tidyverse)
data <- read_tsv("ps2_q3_log_step.tsv")
print(head(data))
data <- data %>% mutate(r = log10(r+1))

# r <- data$r
# C <- data$C
# file <- "ps2_q3_C.png"
# png(file, width = 800, height = 600)  # Open a PNG graphics device
# plot(r, C, pch = 21, bg = "blue", col = "black", cex = 1.5, 
#      main = "Rewires and clustering coefficient for Berkeley graph config models", 
#      xlab = "Log10 number of rewires [log10(r)]", ylab = "Clustering coefficient (C)", 
#      cex.lab = 1.5)  # Increase the axis label font size
# abline(h=0.027679, col="red", lty=2)
# legend("topright", legend="C at 20m rewires", col="red", lty=2, cex=1.5)
# dev.off()

# r <- data$r
# C <- data$C
# file <- "ps2_q3_C.png"
# png(file, width = 800, height = 600)  # Open a PNG graphics device
# plot(r, C, pch = 21, bg = "blue", col = "black", cex = 1.5, 
#      main = "Rewires and clustering coefficient for Berkeley graph config models", 
#      xlab = "Number of rewires (r)", ylab = "Clustering coefficient (C)", 
#      cex.lab = 1.5, xaxt = 'n', xlim = c(-0.25, 9.25))  # Increase the axis label font size
# axis(1, at = 0:9, labels = c(0, 10^c(1:9)))
# abline(h=0.027679, col="red", lty=2)
# legend("topright", legend="C at 20m rewires", col="red", lty=2, cex=1.5)
# dev.off()

r <- data$r
l_mu <- data$l_mu
file <- "ps2_q3_lmu.png"
png(file, width = 800, height = 600)  # Open a PNG graphics device
plot(r, l_mu, pch = 21, bg = "blue", col = "black", cex = 1.5, 
     main = "Rewires and mean geodesic path length for Berkeley graph config models", 
     xlab = "Number of rewires (r)", ylab = "Mean geodesic path length (<l>)", 
     cex.lab = 1.5, xaxt = 'n', xlim = c(-0.25, 9.25))  # Increase the axis label font size
axis(1, at = 0:9, labels = c(0, 10^c(1:9)))
abline(h=2.426839, col="red", lty=2)
legend("topright", legend="<l> at 20m rewires", col="red", lty=2, cex=1.5)
dev.off()