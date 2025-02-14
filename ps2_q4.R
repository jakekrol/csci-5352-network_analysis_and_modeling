# library(igraph)
# library(tidyverse)

# # read graphs
# cat("social network\n")
# g_social <- read_graph("S2Anonymized.tsv", format = "edgelist", directed = FALSE)
# cat("food web\n")
# print(summary(g_social))
# g_food_web <- read_tsv("ps2-chengjiang_shale-food_web.tsv", col_names = FALSE) %>%
#     graph_from_data_frame(directed = FALSE)
# print(summary(g_food_web))
# cat("mouse visual cortex\n")
# g_mouse <- read_graph("mouse_visual.cortex_1.graphml", format = "graphml")
# g_mouse <- as_undirected(g_mouse, mode = "collapse")
# print(summary(g_mouse))

# graphs <- list("social" = g_social, "food" = g_food_web, "connectome" = g_mouse)

# # loop over graphs
# for (name in names(graphs)) {
#     # init
#     g <- graphs[[name]]
#     m <- gsize(g)
#     r <- 0
#     file <- paste0("ps2_q4_", name, ".tsv")
#     cat("Graph: ", name, "Edges: ", m, "File: ", file, "\n")
#     write("r\tC\tl_mu", file, append=TRUE)

#     # compute original clustering coef and mean geodes
#     C <- transitivity(g, type = "global")
#     l_mu <-  mean_distance(g, directed = FALSE, unconnected = TRUE, weights = NA)
#     write(paste0(r, "\t", C, "\t", l_mu), file ,append=TRUE)
#     # first config model
#     r_cf1 <- 20 * m
#     G_cf1 <- rewire(g, keeping_degseq(niter=r_cf1))
#     C <- transitivity(G_cf1, type = "global")
#     l_mu <-  mean_distance(G_cf1, directed = FALSE, unconnected = TRUE, weights = NA)
#     write(paste0(r_cf1, "\t", C, "\t", l_mu), file ,append=TRUE)
#     # next 1000 config models
#     r_cf <- r_cf1
#     G_cfi <- G_cf1
#     for (i in 1:999) {
#         G_cfi <- rewire(G_cfi, keeping_degseq(niter=2 * m))
#         C <- transitivity(G_cfi, type = "global")
#         l_mu <-  mean_distance(G_cfi, directed = FALSE, unconnected = TRUE, weights = NA)
#         r_cf <- r_cf + (2 * m)
#         write(paste0(r_cf, "\t", C, "\t", l_mu), file ,append=TRUE)
#     }
# }

# quit()

# plot config model C and <l> distribution and mark empirical values
FONT_AXIS_LABEL <- 1.7
FONT_AXIS_TICKS <- 1.5
library(tidyverse)
data <- read_tsv("ps2_q4_social.tsv")
png("ps2_q4_social.png", width = 800, height = 600)
par(mfrow=c(3,2))
## social
# C
hist(data$C, breaks=30, main = "Social network clustering coefficient", xlab = "Clustering coefficient (C)", ylab = "Count", col = "blue", xaxt = "n", cex.lab=FONT_AXIS_LABEL, cex.axis=FONT_AXIS_TICKS)
axis(1, at = seq(min(data$C), max(data$C), length.out = 6) |> round(2), cex.axis=FONT_AXIS_TICKS)
abline(v=0.329, col="red", lwd=2)
legend("topright", legend="C empirical", col="red", lwd=2, cex=1.5)
# lmu
hist(data$l_mu, breaks=30, main = "Social network mean geodesic path length", xlab = "Mean geodesic path length (<l>)", ylab = "Count", col = "blue", xaxt='n',cex.lab=FONT_AXIS_LABEL, cex.axis=FONT_AXIS_TICKS)
axis(1, at = seq(min(data$l_mu), max(data$l_mu), length.out = 6) |> round(2), cex.axis=FONT_AXIS_TICKS)
abline(v=2.878, col="red", lwd=2)
legend("topright", legend="<l> empirical", col="red", lwd=2, cex=1.5)
## food
data <- read_tsv("ps2_q4_food.tsv")
# C
hist(data$C, breaks=30, main = "Food web clustering coefficient", xlab = "Clustering coefficient (C)", ylab = "Count", col = "blue", xaxt = "n",cex.lab=FONT_AXIS_LABEL, cex.axis=FONT_AXIS_TICKS)
axis(1, at = seq(min(data$C), max(data$C), length.out = 6) |> round(2), cex.axis=FONT_AXIS_TICKS) 
abline(v=0.746, col="red", lwd=2)
legend("topright", legend="C empirical", col="red", lwd=2, cex=1.5)
# lmu
hist(data$l_mu, breaks=30, main = "Food web mean geodesic path length", xlab = "Mean geodesic path length (<l>)", ylab = "Count", col = "blue", xaxt='n', cex.lab=FONT_AXIS_LABEL, cex.axis=FONT_AXIS_TICKS)
axis(1, at = seq(min(data$l_mu), max(data$l_mu), length.out = 6) |> round(2), cex.axis=FONT_AXIS_TICKS)
abline(v=3.14, col="red", lwd=2)
legend("topright", legend="<l> empirical", col="red", lwd=2, cex=1.5)
## mouse
data <- read_tsv("ps2_q4_connectome.tsv")
# C
hist(data$C, breaks=10, main = "Mouse visual cortex clustering coefficient", xlab = "Clustering coefficient (C)", ylab = "Count", col = "blue", xaxt = "n",cex.lab=FONT_AXIS_LABEL, cex.axis=FONT_AXIS_TICKS)
axis(1, at = seq(min(data$C), max(data$C), length.out = 6) |> round(2), cex.axis=FONT_AXIS_TICKS)
abline(v=0.022, col="red", lwd=2)
legend("topright", legend="C empirical", col="red", lwd=2, cex=1.5)
# lmu
hist(data$l_mu, breaks=30, main = "Mouse visual cortex mean geodesic path length", xlab = "Mean geodesic path length (<l>)", ylab = "Count", col = "blue", xaxt='n',cex.lab=FONT_AXIS_LABEL, cex.axis=FONT_AXIS_TICKS)
axis(1, at = seq(min(data$l_mu), max(data$l_mu), length.out = 6) |> round(2), cex.axis=FONT_AXIS_TICKS)
abline(v=2.94, col="red", lwd=2)
legend("topright", legend="<l> empirical", col="red", lwd=2, cex=1.5)
dev.off()
