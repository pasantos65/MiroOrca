"""
/api/report — Report Domain
Handles report generation and post-simulation agent chat.
"""

from flask import request, jsonify
from . import report_bp
from ..models.task import TaskManager
from ..services.report_agent import ReportAgent
from ..config import config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
task_manager = TaskManager()
report_agent = ReportAgent()


@report_bp.route("/generate", methods=["POST"])
def generate_report():
    """
    Start report generation from simulation logs.
    Async — returns task_id to poll.
    Body: { simulation_id }
    Returns: { task_id }
    """
    data = request.get_json()
    if not data or "simulation_id" not in data:
        return jsonify({"error": "simulation_id is required"}), 400

    task_id = task_manager.create_task("report_generate")

    # TODO: launch ReportAgent as async task

    return jsonify({
        "status": "started",
        "task_id": task_id,
        "message": "Report generation started. Poll /api/report/status/<task_id>."
    })


@report_bp.route("/status/<task_id>", methods=["GET"])
def report_status(task_id):
    """
    Poll report generation progress.
    Returns: { task_id, status, progress_pct, message }
    """
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict())


@report_bp.route("/result", methods=["GET"])
def report_result():
    """
    Get the completed prediction report.
    Query param: simulation_id
    Returns: {
        simulation_id,
        verdict: { score, confidence, summary },
        sentiment_arc: [ { round, score } ],
        top_agents: [ { name, influence, platform } ],
        controversies: [ { topic, intensity } ],
        report_markdown: "..."
    }
    """
    simulation_id = request.args.get("simulation_id")
    if not simulation_id:
        return jsonify({"error": "simulation_id is required"}), 400

    # TODO: load report from saved JSON + markdown files

    return jsonify({
        "simulation_id": simulation_id,
        "verdict": {
            "score": None,
            "confidence": None,
            "summary": "Report not yet generated."
        },
        "sentiment_arc": [],
        "top_agents": [],
        "controversies": [],
        "report_markdown": ""
    })


@report_bp.route("/agents", methods=["GET"])
def list_agents():
    """
    List all agents from the completed simulation.
    Query param: simulation_id
    Returns: { agents: [ { id, name, platform, personality, influence_score } ] }
    """
    simulation_id = request.args.get("simulation_id")
    if not simulation_id:
        return jsonify({"error": "simulation_id is required"}), 400

    # TODO: load from profiles.json

    return jsonify({
        "simulation_id": simulation_id,
        "agents": [],
        "count": 0
    })


@report_bp.route("/chat", methods=["POST"])
def chat_with_report_agent():
    """
    Send a follow-up question to the ReportAgent.
    Body: { simulation_id, message }
    Returns: { reply }
    """
    data = request.get_json()
    if not data or "message" not in data or "simulation_id" not in data:
        return jsonify({"error": "simulation_id and message are required"}), 400

    # TODO: route to ReportAgent ReACT loop

    return jsonify({
        "reply": "ReportAgent chat not yet implemented.",
        "simulation_id": data["simulation_id"]
    })


@report_bp.route("/agent/chat", methods=["POST"])
def chat_with_agent():
    """
    Chat directly with a specific simulated agent.
    Body: { simulation_id, agent_id, message }
    Returns: { agent_id, agent_name, reply }
    """
    data = request.get_json()
    required = {"simulation_id", "agent_id", "message"}
    if not data or not required.issubset(data.keys()):
        return jsonify({"error": "simulation_id, agent_id, and message are required"}), 400

    # TODO: load agent profile + history, generate in-character reply

    return jsonify({
        "agent_id": data["agent_id"],
        "agent_name": "Unknown",
        "reply": "Individual agent chat not yet implemented.",
        "simulation_id": data["simulation_id"]
    })
