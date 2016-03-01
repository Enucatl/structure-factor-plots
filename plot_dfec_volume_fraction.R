#!/usr/bin/env Rscript

library(reshape2)
library(data.table)
library(jsonlite)
library(argparse)
library(ggplot2)

theme_set(theme_bw(base_size=24) + theme(
    legend.key.size=unit(1, 'lines'),
    text=element_text(face='plain', family='CM Roman'),
    legend.title=element_text(face='plain'),
    axis.line=element_line(color='black'),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    legend.key = element_blank(),
    #legend.position = "top",
    #legend.direction = "vertical",
    panel.border = element_blank()
))

parser <- ArgumentParser(description='plot fit prediction')
parser$add_argument('summary', nargs=1)
parser$add_argument('output', nargs=1)
args <- parser$parse_args()

summary = melt(fread(args$summary), id.vars="volume_fraction")
print(summary)

plot = ggplot(summary, aes(colour=variable)) + 
    geom_line(aes(x=volume_fraction, y=value, group=variable), size=1) +
    labs(
         x="volume fraction",
         y="dark field extinction coefficient [1/m]"
         )

width = 14
factor = 0.8
height = width * factor
X11(width=width, height=height)
print(plot)
warnings()
ggsave(args$output, plot, width=width, height=height, dpi=600)
invisible(readLines(con="stdin", 1))
