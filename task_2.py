import json
import time
from datasketch import HyperLogLog


def load_ips_from_json_log(file_path):
    # Завантажує IP-адреси з лог-файлу, ігноруючи некоректні рядки.
    
    ips = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                log = json.loads(line)
                ip = log.get("remote_addr")
                if ip:
                    ips.append(ip)
            except json.JSONDecodeError:
                continue  # Пропускаємо некоректні рядки
    return ips


def exact_count(ips):
    # Точний підрахунок унікальних IP-адрес.
    
    start_time = time.time()
    unique_count = len(set(ips))
    elapsed_time = time.time() - start_time
    return unique_count, elapsed_time


def hyperloglog_count(ips):
    #  Приблизний підрахунок унікальних IP-адрес за допомогою HyperLogLog.
    
    hll = HyperLogLog(p=14)  # точність ~0.81%
    start_time = time.time()
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    unique_count = len(hll)
    elapsed_time = time.time() - start_time
    return unique_count, elapsed_time


def compare_methods(file_path):
    # Порівнює точний та HyperLogLog підрахунок унікальних IP-адрес.
    
    ips = load_ips_from_json_log(file_path)

    exact, exact_time = exact_count(ips)
    approx, hll_time = hyperloglog_count(ips)

    print("Результати порівняння:")
    print(f"{'':30} {'Точний підрахунок':>20} {'HyperLogLog':>15}")
    print(f"{'Унікальні елементи':30} {float(exact):>20.1f} {float(approx):>15.1f}")
    print(f"{'Час виконання (сек.)':30} {exact_time:>20.2f} {hll_time:>15.2f}")


if __name__ == "__main__":
    # Шлях до лог-файлу
    compare_methods("lms-stage-access.log")