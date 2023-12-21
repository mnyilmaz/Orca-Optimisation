'''
Ant Colony Optimization

Ant Colony Optimization (ACO), doğadaki karınca kolonilerinin davranışından esinlenerek geliştirilmiş 
bir optimizasyon algoritmasıdır. Karıncaların yiyecek kaynağına en kısa yolu bulma yeteneği bu algoritmanın 
temelini oluşturur. ACO, özellikle yol bulma, rota planlama ve benzeri optimizasyon problemleri için uygundur.


# Feromon Etkisi
    1. Karınca geçtiği yolda feromon izi bırakır. Bu iz koku temellidir. Diğer karıncalar takip edebilir.
    2. Yolun başarısı feromon oranına da bağlıdır. Yüksek seviyeli feromon içeren yolların başarı oranı daha
    yüksektir. Daha çok karıncanın o yolu kullandığı anlamına gelir.
    3. Bir karınca yol seçecekse bunda feromon etkisi çok yüksek olur. Kokunun yoğun olduğu yöne gitme eğilimindedir.
    Yine de kokunun daha az olduğu alana yönelebilir, ihtimaller arasındadır. Stokastik bir yaklaşım sergiler.
    4. Karınca seçimi ve yol devam ettikçe süreç de devam eder. Her iterasyon sonucu en iyi yolun miktarı artar.
    -> Birinci karıncanın geçmesi ilk iterasyon, 4. karıncanın geçmesi 4. iterasyon gibi...
    
# Formül

    # Feromon güncellemesi
        next_feromon = (1 - evaporaiton_rate) * current_feromon + total_feromon
    
        current_feromon = İterasyon t'de i ve j arasındaki feromon miktarı
        evaporation_rate = Feromon buharlaşma oranı 0 < p < 1
        total_feromon = Bu iterasyonda i ve j arasına bırakılan toplam feromon miktarı
        -> Bütün feromon miktarları belirli bir yolda bırakılan (i ve j arasındaki) feromon miktarını ifade eder.
        
    # Yol seçimi
        probability_ij = t_ij(alpha) * n_ij(beta) / sum(t_ij(alpha) * n_ij(beta))
        
        probability_ij = i'den j'ye geçiş olasılığı
        alpha , beta = Feromon önemini ve feromon uzaklık bilgisini belirleyen parametreler
        n_ij = i'den j'ye geçiş çekiciliği (1/uzaklık gibi)
        
# Optimizasyon
    Katil balinaların yemek peşinde oldukları gözleri sırasında en iyi yolu bulmaları gerekir. Bunda en önemli 
    etkenlerden birisi de yemeğin bıraktığı iz yani feromon miktarıdır. 
    

'''


import random
import numpy as np

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Initialize the Ant Colony Optimization algorithm.

        :param distances: 2D numpy array of distances. The index [i, j] is the distance from city i to j.
        :param n_ants: Number of ants to run per iteration.
        :param n_best: Number of best ants who deposit pheromone.
        :param n_iterations: Number of iterations to run the algorithm for.
        :param decay: Rate at which pheromone decays. The higher the value, the faster it decays.
        :param alpha: Influence of pheromone on direction.
        :param beta: Influence of distance on direction.
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone * self.decay
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)

        # Check if row contains NaN and handle it
        if np.isnan(row).any():
            row = np.nan_to_num(row)  # Replace NaN with zero

        total = row.sum()
        if total == 0:
            norm_row = np.ones(len(row)) / len(row)  # Uniform probabilities if total is 0
        else:
            norm_row = row / total

        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move


# This function should be outside the AntColony class
def np_choice(a, size, replace=True, p=None):
    return np.array(np.random.choice(a, size=size, replace=replace, p=p))

# This function should also be outside the AntColony class
def run_aco_multiple_times(distances, num_runs=100):
    shortest_paths = []
    for _ in range(num_runs):
        aco = AntColony(distances, 10, 3, 100, 0.95, alpha=1, beta=2)
        shortest_path = aco.run()
        shortest_paths.append(shortest_path[1])  # Store the length of the shortest path

    return shortest_paths

# Example usage
distances = np.random.rand(-64,1, -68)
distances = distances + distances.T  # Make it symmetric
np.fill_diagonal(distances, 0)  # Zero diagonal

shortest_paths = run_aco_multiple_times(distances, 100)
mean_length = np.mean(shortest_paths)
std_dev_length = np.std(shortest_paths)

print("Mean length of shortest path: ", mean_length)
print("Standard deviation: ", std_dev_length)

import numpy as np

def calculate_distance(coord1, coord2):
    """İki koordinat arasındaki doğrusal mesafeyi hesaplar."""
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

def create_distance_matrix(coords):
    """Koordinatlar listesinden mesafe matrisi oluşturur."""
    n = len(coords)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = calculate_distance(coords[i], coords[j])
    return distance_matrix

# Koordinatların tanımlanması
coords = [(-64.8, -64.1), (-34.9, -56.2)]  # Başlangıç ve bitiş koordinatları
# Ara noktaları buraya ekleyebilirsiniz, örneğin: coords.append((x, y))

# Mesafe matrisinin oluşturulması
distances = create_distance_matrix(coords)

