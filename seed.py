from datetime import date
from app import app
from models import db, GPU, BenchmarkSuite, BenchmarkResult


GPUS = [
    dict(name="RTX 4090",       manufacturer="NVIDIA", vram_gb=24, base_clock_mhz=2235, boost_clock_mhz=2520, release_year=2022, msrp=1599.0),
    dict(name="RTX 4080 Super", manufacturer="NVIDIA", vram_gb=16, base_clock_mhz=2295, boost_clock_mhz=2550, release_year=2024, msrp=999.0),
    dict(name="RTX 4070 Ti",    manufacturer="NVIDIA", vram_gb=12, base_clock_mhz=2310, boost_clock_mhz=2610, release_year=2023, msrp=799.0),
    dict(name="RTX 3080",       manufacturer="NVIDIA", vram_gb=10, base_clock_mhz=1440, boost_clock_mhz=1710, release_year=2020, msrp=699.0),
    dict(name="RX 7900 XTX",    manufacturer="AMD",    vram_gb=24, base_clock_mhz=1855, boost_clock_mhz=2500, release_year=2022, msrp=999.0),
    dict(name="RX 7800 XT",     manufacturer="AMD",    vram_gb=16, base_clock_mhz=1624, boost_clock_mhz=2430, release_year=2023, msrp=499.0),
    dict(name="RX 6800 XT",     manufacturer="AMD",    vram_gb=16, base_clock_mhz=1825, boost_clock_mhz=2250, release_year=2020, msrp=649.0),
    dict(name="Arc A770",       manufacturer="Intel",  vram_gb=16, base_clock_mhz=2100, boost_clock_mhz=2100, release_year=2022, msrp=349.0),
    dict(name="Arc A750",       manufacturer="Intel",  vram_gb=8,  base_clock_mhz=2050, boost_clock_mhz=2050, release_year=2022, msrp=289.0),
]

SUITES = [
    dict(name="3DMark Time Spy",      version="2.0",  type="Synthetic"),
    dict(name="3DMark Fire Strike",   version="1.1",  type="Synthetic"),
    dict(name="Unigine Superposition", version="1.x", type="Stress Test"),
    dict(name="FurMark",              version="2.3",  type="Stress Test"),
    dict(name="Shadow of the Tomb Raider", version="1.0", type="Game Sim"),
    dict(name="Cyberpunk 2077 Benchmark", version="2.1", type="Game Sim"),
]

RESULTS = [
    dict(gpu=0, suite=0, score=25410, fps_avg=None,  fps_min=None,  temp_max_c=72.0, power_draw_watts=420.0, resolution="4K",    date_tested=date(2024, 1, 15), notes="Stock settings"),
    dict(gpu=0, suite=4, score=None,  fps_avg=138.2, fps_min=112.0, temp_max_c=74.0, power_draw_watts=430.0, resolution="4K",    date_tested=date(2024, 1, 16), notes="Max settings, RT off"),
    dict(gpu=0, suite=5, score=None,  fps_avg=85.4,  fps_min=67.0,  temp_max_c=76.0, power_draw_watts=440.0, resolution="4K",    date_tested=date(2024, 2,  1), notes="RT Ultra, DLSS Quality"),
    dict(gpu=1, suite=0, score=20180, fps_avg=None,  fps_min=None,  temp_max_c=68.0, power_draw_watts=310.0, resolution="1440p", date_tested=date(2024, 3,  5), notes=None),
    dict(gpu=1, suite=4, score=None,  fps_avg=128.7, fps_min=104.5, temp_max_c=70.0, power_draw_watts=315.0, resolution="1440p", date_tested=date(2024, 3,  6), notes=None),
    dict(gpu=2, suite=1, score=38200, fps_avg=None,  fps_min=None,  temp_max_c=65.0, power_draw_watts=285.0, resolution="1080p", date_tested=date(2023, 9, 20), notes=None),
    dict(gpu=2, suite=5, score=None,  fps_avg=92.1,  fps_min=74.3,  temp_max_c=67.0, power_draw_watts=290.0, resolution="1440p", date_tested=date(2023, 9, 21), notes="DLSS Balanced"),
    dict(gpu=3, suite=0, score=14820, fps_avg=None,  fps_min=None,  temp_max_c=80.0, power_draw_watts=350.0, resolution="1440p", date_tested=date(2022, 6, 10), notes=None),
    dict(gpu=3, suite=2, score=None,  fps_avg=None,  fps_min=None,  temp_max_c=88.0, power_draw_watts=360.0, resolution="4K",    date_tested=date(2022, 6, 11), notes="Stress test 20 min"),
    dict(gpu=4, suite=0, score=22540, fps_avg=None,  fps_min=None,  temp_max_c=69.0, power_draw_watts=355.0, resolution="4K",    date_tested=date(2023, 4, 18), notes=None),
    dict(gpu=4, suite=4, score=None,  fps_avg=119.3, fps_min=95.8,  temp_max_c=71.0, power_draw_watts=360.0, resolution="4K",    date_tested=date(2023, 4, 19), notes="Max settings"),
    dict(gpu=4, suite=3, score=None,  fps_avg=None,  fps_min=None,  temp_max_c=85.0, power_draw_watts=375.0, resolution="4K",    date_tested=date(2023, 4, 20), notes="FurMark burn-in"),
    dict(gpu=5, suite=1, score=34750, fps_avg=None,  fps_min=None,  temp_max_c=66.0, power_draw_watts=263.0, resolution="1080p", date_tested=date(2023, 11, 2), notes=None),
    dict(gpu=5, suite=5, score=None,  fps_avg=78.6,  fps_min=60.2,  temp_max_c=68.0, power_draw_watts=270.0, resolution="1440p", date_tested=date(2023, 11, 3), notes="RSR on"),
    dict(gpu=6, suite=0, score=13990, fps_avg=None,  fps_min=None,  temp_max_c=75.0, power_draw_watts=300.0, resolution="1440p", date_tested=date(2022, 3, 22), notes=None),
    dict(gpu=7, suite=1, score=29400, fps_avg=None,  fps_min=None,  temp_max_c=78.0, power_draw_watts=225.0, resolution="1080p", date_tested=date(2023, 7, 14), notes="Driver 31.0.101"),
    dict(gpu=7, suite=4, score=None,  fps_avg=73.5,  fps_min=58.1,  temp_max_c=80.0, power_draw_watts=228.0, resolution="1080p", date_tested=date(2023, 7, 15), notes=None),
    dict(gpu=8, suite=1, score=24800, fps_avg=None,  fps_min=None,  temp_max_c=76.0, power_draw_watts=190.0, resolution="1080p", date_tested=date(2023, 7, 16), notes=None),
]


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables created.")

        gpu_objs = [GPU(**g) for g in GPUS]
        db.session.add_all(gpu_objs)
        db.session.flush()

        suite_objs = [BenchmarkSuite(**s) for s in SUITES]
        db.session.add_all(suite_objs)
        db.session.flush()

        for r in RESULTS:
            result = BenchmarkResult(
                gpu_id=gpu_objs[r["gpu"]].gpu_id,
                suite_id=suite_objs[r["suite"]].suite_id,
                score=r.get("score"),
                fps_avg=r.get("fps_avg"),
                fps_min=r.get("fps_min"),
                temp_max_c=r.get("temp_max_c"),
                power_draw_watts=r.get("power_draw_watts"),
                resolution=r["resolution"],
                date_tested=r["date_tested"],
                notes=r.get("notes"),
            )
            db.session.add(result)

        db.session.commit()
        print(f"Seeded {len(gpu_objs)} GPUs, {len(suite_objs)} suites, {len(RESULTS)} results.")


if __name__ == "__main__":
    seed()
