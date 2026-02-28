import folium
from folium import plugins
import itertools
import datetime as dt

def crtaj(vector, frute_iz_res):
    """
    Crta rute na interaktivnoj mapi i sprema kao HTML
    
    vector: lista sa koordinatama [lat, lon]
    frute_iz_res: rečnik sa rutama
    """
    
    # Ekstrakcija ruta i povratnih čvorova
    b = []
    c = []
    for ruta in frute_iz_res:
        a = []
        for j in ruta[0]:
            a.append(abs(j))
        b.append(a)
        c.append(frute_iz_res[ruta][2])
    
    lis = b
    rute_broj = len(frute_iz_res)
    
    # Boje za svaku rutu
    color_list = ["green", "red", "blue", "purple", "orange", "darkred", "darkblue", "darkgreen"]
    color_cycle = itertools.cycle(color_list)
    
    # Kreiraj mapu - centar na prosečnu lokaciju
    all_coords = [vector[i] for i in range(1, len(vector))]
    avg_lat = sum(c[0] for c in all_coords) / len(all_coords)
    avg_lon = sum(c[1] for c in all_coords) / len(all_coords)
    
    map_rute = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Prikazi svaku rutu
    for route_idx, fields in enumerate(lis):
        color = next(color_cycle)
        
        # Ekstrakcija koordinata
        coords = []
        for node_id in fields:
            if node_id > 0 and node_id < len(vector):
                lat, lon = vector[node_id]
                coords.append([lat, lon])
        
        if len(coords) == 0:
            continue
        
        # Crtaj liniju za rutu
        folium.PolyLine(
            coords,
            color=color,
            weight=3,
            opacity=0.8,
            popup=f'Ruta {route_idx + 1}'
        ).add_to(map_rute)
        
        # Dodaj markere za čvorove
        for idx, (lat, lon) in enumerate(coords):
            node_num = fields[idx]
            
            # Različite ikonice za dostave i povratne lokacije
            if idx < c[route_idx]:
                marker_color = 'blue'
                icon_prefix = '📦'
            else:
                marker_color = 'red'
                icon_prefix = '↩️'
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                popup=f'<b>Čvor {node_num}</b><br>Ruta: {route_idx + 1}',
                color=marker_color,
                fill=True,
                fillColor=marker_color,
                fillOpacity=0.7,
                weight=2
            ).add_to(map_rute)
            
            # Dodaj tekst sa brojem čvora
            folium.Marker(
                location=[lat, lon],
                popup=str(node_num),
                icon=folium.Icon(icon='info-sign', color='gray')
            ).add_to(map_rute)
    
    # Spremi mapu kao HTML
    output_file = 'data/rute_mapa.html'
    map_rute.save(output_file)
    print(f"\n✅ Mapa sa rutama je sprema na: {output_file}")
    print(f"📊 Broj ruta: {rute_broj}")
    
    return map_rute

#crtaj(vector, lis, 2)
