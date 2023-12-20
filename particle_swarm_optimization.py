'''
Particle Swarm Optimization Algorithm 

PSO'da, p_best ve g_best değerleri, genellikle bir optimizasyon probleminin çözüm kalitesini temsil eder. 
Bu değerlerin neyi ifade ettiğini ve düşük olmalarının anlamını anlamak için, önce bu değerlerin nasıl 
hesaplandığını ve neyi temsil ettiğini bilmek önemlidir:

p_best Değerleri: Her parçacığın (particle) şimdiye kadar bulduğu en iyi çözümü temsil eder. 
Bu, parçacığın arama sürecinde ulaştığı en iyi performansı gösterir.

g_best Değeri: Tüm parçacıklar arasında bulunan en iyi çözümü temsil eder. 
Bu, algoritmanın şu ana kadar bulduğu en iyi global çözümdür.


# Formül
    v_next = w . v + c1 . r1(p_best -x) + c2 . r2(g_best - x)
    x_next = x + v_next

    w: Eylemsizlik ağırlığı -> 0.5 - 0.9 arasında bir değer seçilir
    v: Mevcut hız (parçacığın)
    x: Mevcut konum (parçacığın)
    c1: Bilişsel katsayı -> 1.5 - 2 aralığında herhangi bir değer uygundur
    c2: Sosyal katsayı -> 1.5 - 2 aralığında herhangi bir değer uygundur
    p_best: Parçacığın kişisel en iyi sonucu
    g_best: Tüm parçacıkların en iyi sonucu


# Notlar
    -> Her hesaplama için w, c1 ve c2 değerleri sabit tutulur.
    -> w değeri balinaların önceki yüzme yönlerini ne kadar koruyacaklarını belirler.
    -> c1 ve c2 bilişsel ve sosyal öğrenme katsayılarıdır.
    -> r1 ve r2 0 - 1 aralığında rastgele sayılardır.
    
    
# Optimizasyon Problemi
    Bu problem kapsamında katil balinaların (orka) göç optimizasyonu için hesaplamalar yapılacaktır. Tip B olarak 
    seçilmiş katil balinalar için şu verilerin mevcudiyeti söz konusudur:
    1. Pod size: Sürü kalabalığı göçü olumlu etkiler
    2. Grandmother Effect: Sürüde bulunan tecrübeli dişi liderin varlığı göçü olumlu etkiler
    3. Genellikle fok ve diğer her şeyi yerler
    4. İnsanlar ve hastalıklar dışında apex predators olarak bilinirler, kimse onlara bulaşmaz
    5. Hız: Ortalama 56 km/h 
    6: Başlangıç konumu -64.8 enlem, -64.1 boylam
    7: Bitiş konumu -34.9 enlem, -56.2 boylam


# Parametre Belirteçleri

    pod_size = Sürüdeki katil balina sayısı
    grandmother_effect = Dişi lider (büyükanne) varlığı -> 0.25
    climate_change = İklim değişimi etkisi -> 0.15 etki eder
    threat_existence = Tehdit varlığı -> 0.5 etki eder
    p_best = Parçacık başlangıçta (-64.8, -64.1) konumunda olacak
    g_best = Bütün parçacıklar başlangıçta (-64.8, -64.1) konumunda olacaklar 
    
    
# Ortalama ve Standart Sapma Yorumları
    Ortalama: Veri setindeki verilerin ortalama değeri
    Standart Sapma: Veri setindeki verilerin ortalamadan farklılığı
    1. En düşük değeri bulma üzerinde bir optimizasyon gerçekleştiriliyorsa ortalamanın düşük olması iyidir.
    2. Hem ortalama hem standart sapma düşükse arama uzayı yeterince keşfedilmemiş olabilir. Birbirine benzer
    çözümlerin varlığı mevcuttur. 

'''

import random
import statistics

class Particle:
    def __init__(self, bounds):
        self.position = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
        self.velocity = [random.uniform(-1, 1) for _ in range(len(bounds))]
        self.pbest_position = self.position.copy()
        self.pbest_value = float('inf')

    def update_velocity(self, gbest_position, w, c1, c2):
        for i in range(len(self.position)):
            r1, r2 = random.random(), random.random()
            cognitive_velocity = c1 * r1 * (self.pbest_position[i] - self.position[i])
            social_velocity = c2 * r2 * (gbest_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity

    def move(self):
        self.position = [self.position[i] + self.velocity[i] for i in range(len(self.position))]
        
def orca_distance_score(x, y, target_x, target_y):
    # Ortalama orka boyu 7 metre
    score = random.uniform(1,2)
    distance = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
    if 3 <= distance <= 10:
        score = random.uniform(4, 5)

    return score

def resource_distance_score(x, y, target_x, target_y):
    # 2 orka uzaklıkta
    score = random.uniform(1,2)
    distance = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
    if distance >= 0:
        if distance <= 16:
            score = random.uniform(4,5)
        
    return score

def experience_score(pod_size, grandmother_effect):
    score = random.uniform(1,2)
    
    if pod_size * grandmother_effect > 0:
        score = random.uniform(4,5)
        
    return score

def threat_score(climate_change, threat_existence):
    score = random.uniform(3,4)
    
    if climate_change == 0 and threat_existence == 0:
        score = random.uniform(4,5)
    elif climate_change == 1 and threat_existence == 0:
        score = random.uniform(2,3)
    elif climate_change == 0 and threat_existence == 1:
        score = random.uniform(3,4)
    
    return score
     

def evaluate(position, pod_size, grandmother_effect, climate_change, threat_existence):
    x, y = position
    target_x = 1
    target_y = 1
    distance_evaluation = orca_distance_score(x, y, target_x, target_y)
    resource_evaluation = resource_distance_score(x, y, target_x, target_y)
    pod_evaluation = experience_score(pod_size, grandmother_effect)
    env_evaluation = threat_score(climate_change, threat_existence)
    # Skor ağırlıkları
    mean = (distance_evaluation * 0.1 + resource_evaluation * 0.3 + pod_evaluation * 0.4 + env_evaluation * 0.2) / 4
    
    return mean

    
# PSO algoritması
def pso(num_particles, bounds, num_iterations, w, c1, c2, pod_size, grandmother_effect, climate_change, threat_existence):
    particles = [Particle(bounds) for _ in range(num_particles)]
    gbest_position = [0.0, 0.0]
    gbest_value = float('inf')

    for _ in range(num_iterations):
        for particle in particles:
            particle_value = evaluate(particle.position, pod_size, grandmother_effect, climate_change, threat_existence)

            # pbest ve gbest güncellemeleri
            if particle_value < particle.pbest_value:
                particle.pbest_value = particle_value
                particle.pbest_position = particle.position.copy()

            if particle_value < gbest_value:
                gbest_value = particle_value
                gbest_position = particle.position.copy()

        # Hız ve konum güncellemeleri
        for particle in particles:
            particle.update_velocity(gbest_position, w, c1, c2)
            particle.move()

    return particles, gbest_position

if __name__ == "__main__":
    num_particles = 100  # Örnek parçacık sayısı
    bounds = [(-64.8, -34.9), (-64.1, -56.2)]  # Antartika Uruguay arası
    num_iterations = 50
    w = random.uniform(0.5, 0.9) 
    c1, c2 = random.uniform(1.5, 2), random.uniform(1.5, 2)
    pod_size = 30
    grandmother_effect = 1
    climate_change = 1
    threat_existence = 0
    
    particles, gbest_position = pso(num_particles, bounds, num_iterations, w, c1, c2, pod_size, grandmother_effect, climate_change, threat_existence)
    p_best_values = [particle.pbest_value for particle in particles]
    mean_p_best = statistics.mean(p_best_values)
    std_dev_p_best = statistics.stdev(p_best_values)


    print(f"Global Best Position: {gbest_position}")
    for i, particle in enumerate(particles):
        print(f"Particle {i+1} Best Position: {particle.pbest_position}")
    
    print(f"Mean Particle Best Position: {mean_p_best}")
    print(f"Standard Deviation Particle Best Position: {std_dev_p_best}")
