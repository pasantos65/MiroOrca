"""
/api/graph — Knowledge Graph Domain
Handles document upload and knowledge graph extraction.
"""

from flask import request, jsonify
from . import graph_bp
from ..models.task import TaskManager
from ..services.ontology_generator import OntologyGenerator
from ..services.graph_builder import GraphBuilderService
from ..config import config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
task_manager = TaskManager()


@graph_bp.route("/upload", methods=["POST"])
def upload_document():
    """
    Upload a source document (PDF, MD, TXT).
    Returns: { file_id, filename, size_bytes }
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in config.ALLOWED_EXTENSIONS:
        return jsonify({
            "error": f"Unsupported file type: .{ext}",
            "allowed": list(config.ALLOWED_EXTENSIONS)
        }), 400

    # TODO: save file to uploads/<simulation_id>/source/
    # TODO: return file_id for use in /build

    return jsonify({
        "status": "uploaded",
        "filename": file.filename,
        "message": "File received. Call /api/graph/build to begin extraction."
    })


@graph_bp.route("/build", methods=["POST"])
def build_graph():
    """
    Start knowledge graph extraction from uploaded document.
    This is async — returns a task_id to poll for status.
    Body: { file_id, simulation_id, prediction_requirement }
    Returns: { task_id }
    """
    data = request.get_json()
    if not data or "file_id" not in data:
        return jsonify({"error": "file_id is required"}), 400

    # TODO: launch OntologyGenerator + GraphBuilderService as async task
    task_id = task_manager.create_task("graph_build")

    return jsonify({
        "status": "started",
        "task_id": task_id,
        "message": "Graph extraction started. Poll /api/graph/status/<task_id> for progress."
    })


@graph_bp.route("/status/<task_id>", methods=["GET"])
def graph_status(task_id):
    """
    Poll extraction task progress.
    Returns: { task_id, status, progress_pct, message }
    Status values: pending | running | complete | failed
    """
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict())


@graph_bp.route("/result", methods=["GET"])
def graph_result():
    """
    Get the completed knowledge graph summary.
    Query param: simulation_id
    Returns: { entities, relationships, summary }
    """
    simulation_id = request.args.get("simulation_id")
    if not simulation_id:
        return jsonify({"error": "simulation_id is required"}), 400

    # TODO: load graph summary from Neo4j / saved JSON

    return jsonify({
        "simulation_id": simulation_id,
        "entities": [],
        "relationships": [],
        "summary": "Graph result not yet implemented."
    })
