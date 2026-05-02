from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from models import db, GPU, BenchmarkSuite, BenchmarkResult
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///benchmarks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "cs348-gpu-benchmark-tracker"

db.init_app(app)

RESOLUTIONS = ["1080p", "1440p", "4K"]


def parse_result_form(form):
    # clean up form values and convert them before saving
    score_raw = form.get("score", "").strip()
    fps_avg_raw = form.get("fps_avg", "").strip()

    if not score_raw and not fps_avg_raw:
        raise ValueError("Enter at least a Score or Avg FPS for the benchmark result.")

    return {
        "gpu_id": int(form["gpu_id"]),
        "suite_id": int(form["suite_id"]),
        "score": int(score_raw) if score_raw else None,
        "fps_avg": float(fps_avg_raw) if fps_avg_raw else None,
        "fps_min": float(form["fps_min"]) if form.get("fps_min") else None,
        "temp_max_c": float(form["temp_max_c"]) if form.get("temp_max_c") else None,
        "power_draw_watts": float(form["power_draw_watts"]) if form.get("power_draw_watts") else None,
        "resolution": form["resolution"],
        "date_tested": datetime.strptime(form["date_tested"], "%Y-%m-%d").date(),
        "notes": form.get("notes") or None,
    }

@app.route("/")
def index():
    return redirect(url_for("results_list"))


@app.route("/results")
def results_list():
    results = (
        db.session.query(BenchmarkResult)
        .join(GPU)
        .join(BenchmarkSuite)
        .order_by(BenchmarkResult.date_tested.desc())
        .all()
    )
    return render_template("results.html", results=results)

@app.route("/results/add", methods=["GET", "POST"])
def results_add():
    gpus = GPU.query.order_by(GPU.manufacturer, GPU.name).all()
    suites = BenchmarkSuite.query.order_by(BenchmarkSuite.name).all()

    if request.method == "POST":
        try:
            result = BenchmarkResult(**parse_result_form(request.form))
            db.session.add(result)
            # commit only after the full result object is valid
            db.session.commit()
            flash("Result added successfully.", "success")
            return redirect(url_for("results_list"))
        except Exception as e:
            # rollback keeps a bad form submit from partially saving
            db.session.rollback()
            flash(f"Error adding result: {e}", "danger")

    return render_template(
        "result_form.html",
        action="Add",
        result=None,
        gpus=gpus,
        suites=suites,
        resolutions=RESOLUTIONS,
        today=date.today().isoformat(),
    )

@app.route("/results/edit/<int:result_id>", methods=["GET", "POST"])
def results_edit(result_id):
    result = db.get_or_404(BenchmarkResult, result_id)
    gpus = GPU.query.order_by(GPU.manufacturer, GPU.name).all()
    suites = BenchmarkSuite.query.order_by(BenchmarkSuite.name).all()

    if request.method == "POST":
        try:
            form_data = parse_result_form(request.form)
            # update the existing row, then commit it as one transaction
            result.gpu_id = form_data["gpu_id"]
            result.suite_id = form_data["suite_id"]
            result.score = form_data["score"]
            result.fps_avg = form_data["fps_avg"]
            result.fps_min = form_data["fps_min"]
            result.temp_max_c = form_data["temp_max_c"]
            result.power_draw_watts = form_data["power_draw_watts"]
            result.resolution = form_data["resolution"]
            result.date_tested = form_data["date_tested"]
            result.notes = form_data["notes"]
            db.session.commit()
            flash("Result updated successfully.", "success")
            return redirect(url_for("results_list"))
        except Exception as e:
            # if anything fails, keep the old result unchanged
            db.session.rollback()
            flash(f"Error updating result: {e}", "danger")

    return render_template(
        "result_form.html",
        action="Edit",
        result=result,
        gpus=gpus,
        suites=suites,
        resolutions=RESOLUTIONS,
        today=date.today().isoformat(),
    )

@app.route("/results/delete/<int:result_id>", methods=["POST"])
def results_delete(result_id):
    result = db.get_or_404(BenchmarkResult, result_id)
    db.session.delete(result)
    db.session.commit()
    flash("Result deleted.", "warning")
    return redirect(url_for("results_list"))

@app.route("/report")
def report():
    # values for the report filter dropdowns
    manufacturers = [
        row[0]
        for row in db.session.query(GPU.manufacturer)
        .distinct()
        .order_by(GPU.manufacturer)
        .all()
    ]
    gpus = GPU.query.order_by(GPU.manufacturer, GPU.name).all()
    suites = BenchmarkSuite.query.order_by(BenchmarkSuite.name).all()

    f_manufacturer = request.args.get("manufacturer", "")
    f_gpu_id = request.args.get("gpu_id", "")
    f_suite_id = request.args.get("suite_id", "")
    f_resolution = request.args.get("resolution", "")
    f_date_from = request.args.get("date_from", "")
    f_date_to = request.args.get("date_to", "")
    generate = request.args.get("generate")

    rows = []
    stats = None

    if generate:
        # start with the full report query, then add filters the user selected
        query = (
            db.session.query(BenchmarkResult)
            .join(GPU)
            .join(BenchmarkSuite)
        )

        if f_manufacturer:
            query = query.filter(GPU.manufacturer == f_manufacturer)
        if f_gpu_id:
            query = query.filter(BenchmarkResult.gpu_id == int(f_gpu_id))
        if f_suite_id:
            query = query.filter(BenchmarkResult.suite_id == int(f_suite_id))
        if f_resolution:
            query = query.filter(BenchmarkResult.resolution == f_resolution)
        if f_date_from:
            query = query.filter(
                BenchmarkResult.date_tested >= datetime.strptime(f_date_from, "%Y-%m-%d").date()
            )
        if f_date_to:
            query = query.filter(
                BenchmarkResult.date_tested <= datetime.strptime(f_date_to, "%Y-%m-%d").date()
            )

        rows = query.order_by(BenchmarkResult.score.desc(), BenchmarkResult.fps_avg.desc()).all()

        if rows:
            scores = [r.score for r in rows if r.score is not None]
            fpss = [r.fps_avg for r in rows if r.fps_avg is not None]
            temps = [r.temp_max_c for r in rows if r.temp_max_c is not None]
            powers = [r.power_draw_watts for r in rows if r.power_draw_watts is not None]
            scored_rows = [r for r in rows if r.score is not None]
            top = max(scored_rows, key=lambda r: r.score) if scored_rows else None

            stats = {
                "total": len(rows),
                "avg_score": round(sum(scores) / len(scores), 1) if scores else None,
                "avg_fps": round(sum(fpss) / len(fpss), 1) if fpss else None,
                "top_score": top.score if top else None,
                "top_gpu": top.gpu.name if top else None,
                "avg_temp": round(sum(temps) / len(temps), 1) if temps else None,
                "avg_power": round(sum(powers) / len(powers), 1) if powers else None,
            }

    return render_template(
        "report.html",
        manufacturers=manufacturers,
        gpus=gpus,
        suites=suites,
        resolutions=RESOLUTIONS,
        rows=rows,
        stats=stats,
        f_manufacturer=f_manufacturer,
        f_gpu_id=f_gpu_id,
        f_suite_id=f_suite_id,
        f_resolution=f_resolution,
        f_date_from=f_date_from,
        f_date_to=f_date_to,
        generate=generate,
    )


if __name__ == "__main__":
    app.run(debug=True)
