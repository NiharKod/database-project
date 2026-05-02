from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class GPU(db.Model):
    __tablename__ = "gpus"
    # helps the report filter quickly find gpus by brand
    __table_args__ = (
        db.Index("ix_gpus_manufacturer", "manufacturer"),
    )

    gpu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, nullable=False)
    vram_gb = db.Column(db.Integer, nullable=False)
    base_clock_mhz = db.Column(db.Integer, nullable=False)
    boost_clock_mhz = db.Column(db.Integer, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    msrp = db.Column(db.Float, nullable=True)

    results = db.relationship(
        "BenchmarkResult", back_populates="gpu", cascade="all, delete-orphan"
    )


class BenchmarkSuite(db.Model):
    __tablename__ = "benchmark_suites"

    suite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False)

    results = db.relationship(
        "BenchmarkResult", back_populates="suite", cascade="all, delete-orphan"
    )


class BenchmarkResult(db.Model):
    __tablename__ = "benchmark_results"
    # indexes used by the main report filters and date sorting
    __table_args__ = (
        db.Index(
            "ix_results_report_filters",
            "gpu_id",
            "suite_id",
            "resolution",
            "date_tested",
        ),
        db.Index("ix_results_date_tested", "date_tested"),
    )

    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gpu_id = db.Column(db.Integer, db.ForeignKey("gpus.gpu_id"), nullable=False)
    suite_id = db.Column(
        db.Integer, db.ForeignKey("benchmark_suites.suite_id"), nullable=False
    )
    score = db.Column(db.Integer, nullable=True)
    fps_avg = db.Column(db.Float, nullable=True)
    fps_min = db.Column(db.Float, nullable=True)
    temp_max_c = db.Column(db.Float, nullable=True)
    power_draw_watts = db.Column(db.Float, nullable=True)
    resolution = db.Column(db.String, nullable=False)
    date_tested = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    gpu = db.relationship("GPU", back_populates="results")
    suite = db.relationship("BenchmarkSuite", back_populates="results")
