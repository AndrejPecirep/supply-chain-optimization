from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from dataclasses import dataclass
import math

@dataclass
class Location:
    name: str
    lat: float
    lon: float


def haversine_km(a: Location, b: Location) -> float:
    r = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [a.lat, a.lon, b.lat, b.lon])
    dlat, dlon = lat2-lat1, lon2-lon1
    x = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*r*math.asin(math.sqrt(x))


def nearest_neighbor_route(depot: Location, stops: list[Location]) -> tuple[list[str], float]:
    remaining = stops[:]
    current = depot
    route = [depot.name]
    total = 0.0
    while remaining:
        nxt = min(remaining, key=lambda loc: haversine_km(current, loc))
        total += haversine_km(current, nxt)
        route.append(nxt.name)
        current = nxt
        remaining.remove(nxt)
    total += haversine_km(current, depot)
    route.append(depot.name)
    return route, round(total, 2)

if __name__ == '__main__':
    depot = Location('Sarajevo DC', 43.8563, 18.4131)
    stops = [Location('Mostar',43.3438,17.8078), Location('Banja Luka',44.7722,17.1910), Location('Tuzla',44.5384,18.6671)]
    print(nearest_neighbor_route(depot, stops))
