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
import statistics

