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
    
    Orca başlangıçta (-64.8, 0.0) konumunda olacak
    Orca yolun sonunda (-34.9, -56.2) konumunda olacak 


'''

import random
import numpy as np
import math
import statistics

class AntColony:
    def __init__(self, n_waypoints, orcas, n_iterations, decay_rate):
        self.distances = np.random.rand(n_waypoints, n_waypoints)
        self.pheromone = np.ones(self.distances.shape) / n_waypoints
        self.orcas = orcas
        self.n_iterations = n_iterations
        self.decay_rate = decay_rate

    def run(self):
        shortest_path = None
        shortest_path_length = float('inf')
        for _ in range(self.n_iterations):
            for _ in range(self.orcas):
                path, length = self.generate_path()
                if length < shortest_path_length:
                    shortest_path = path
                    shortest_path_length = length
            self.update_pheromone(shortest_path, shortest_path_length)
            self.pheromone *= self.decay_rate
        return shortest_path, shortest_path_length

    def generate_path(self):
        path = [random.randint(0, len(self.distances) - 1)]
        while len(path) < len(self.distances):
            current = path[-1]
            next_node = self.select_next_node(current)
            path.append(next_node)
        path_length = self.calculate_path_length(path)
        return path, path_length

    def select_next_node(self, current):
        probabilities = self.pheromone[current] / self.pheromone[current].sum()
        next_node = np.random.choice(len(self.distances), p=probabilities)
        return next_node

    def calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += self.distances[path[i]][path[i+1]]
        return length

    def update_pheromone(self, path, length):
        for i in range(len(path) - 1):
            self.pheromone[path[i]][path[i+1]] += 1 / length
    

def euclid_algorithm(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Orca'nın başlangıç ve bitiş koordinatları
x1, y1 = -64.8, 0.0
x2, y2 = -34.9, -56.2

# Mesafe hesaplama
distance = euclid_algorithm(x1, x2, y1, y2)
print("Orca'nın göç mesafesi:", distance)

# Example usage
n_waypoints = 5  # TGöç durakları
shortest_path_lengths = []

for i in range (100):
    ant_colony = AntColony(n_waypoints, orcas=10, n_iterations=100, decay_rate=0.8)
    shortest_path, shortest_path_length = ant_colony.run()
    shortest_path_lengths.append(shortest_path_length)
    print(f"En kısa yol: {shortest_path_length}")


mean_shortest_paths = statistics.mean(shortest_path_lengths)
std_dev_shortest_paths = statistics.stdev(shortest_path_lengths)

print(f"En kısa yolların ortalaması: {mean_shortest_paths}")
print(f"En kısa yolların standart sapması: {std_dev_shortest_paths}")
