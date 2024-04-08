n = 10

# Authentication server
server = ("localhost", 5555)

dataset = [[860, 393, 217, 446, 314, 655, 785, 98, 36, 181], [718, 654, 123, 318, 639, 331, 741, 769, 262, 111], [686, 225, 757, 636, 893, 351, 731, 287, 716, 868], [72, 545, 1, 576, 876, 74, 567, 570, 285, 742], [819, 973, 157, 800, 601, 379, 718, 352, 316, 828], [77, 406, 899, 399, 591, 209, 29, 485, 143, 510], [428, 920, 531, 314, 286, 757, 455, 353, 741, 83], [514, 288, 542, 663, 970, 65, 79, 250, 798, 493], [108, 164, 87, 10, 130, 449, 797, 723, 38, 429], [16, 194, 362, 557, 697, 597, 173, 74, 556, 240]]
normalized = [[0.564, 0.258, 0.142, 0.292, 0.206, 0.429, 0.515, 0.064, 0.024, 0.119], [0.429, 0.391, 0.074, 0.19, 0.382, 0.198, 0.443, 0.46, 0.157, 0.066], [0.331, 0.108, 0.365, 0.307, 0.431, 0.169, 0.352, 0.138, 0.345, 0.418], [0.044, 0.333, 0.001, 0.352, 0.535, 0.045, 0.346, 0.348, 0.174, 0.453], [0.399, 0.474, 0.077, 0.39, 0.293, 0.185, 0.35, 0.172, 0.154, 0.403], [0.054, 0.284, 0.628, 0.279, 0.413, 0.146, 0.02, 0.339, 0.1, 0.356], [0.249, 0.535, 0.309, 0.183, 0.166, 0.441, 0.265, 0.205, 0.431, 0.048], [0.298, 0.167, 0.314, 0.384, 0.562, 0.038, 0.046, 0.145, 0.463, 0.286], [0.085, 0.129, 0.069, 0.008, 0.103, 0.354, 0.628, 0.57, 0.03, 0.338], [0.012, 0.148, 0.276, 0.424, 0.531, 0.455, 0.132, 0.056, 0.424, 0.183]]

padded = [
    [int(i * 1000) for i in row] for row in normalized
]