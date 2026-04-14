"""
/api/simulation — Simulation Domain
Handles agent profile generation and simulation run control.
"""

from flask import request, jsonify
from . import simulation_bp
from ..models.task import TaskManager
from ..services.profile_generator import ProfileGenerator
from ..services.simulation_runner import SimulationRunner
from ..config import config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
task_manager = TaskManager()
simulation_runner = SimulationRunner()


@simulation_bp.route("/prepare", methods=["POST"])
def prepare_simulation():
    """
    Generate agent personas and simulation config from the knowledge graph.
    Body: { simulation_id, agent_count (optional) }
    Returns: { task_id }
    """
    data = request.get_json()
    if not data or "simulation_id" not in data:
        return jsonify({"error": "simulation_id is required"}), 400

    agent_count = data.get("agent_count", config.DEFAULT_AGENT_COUNT)
    task_id = task_manager.create_task("simulation_prepare")

    # TODO: launch ProfileGenerator as async task
    logger.info(f"Preparing simulation {data['simulation_id']} with {agent_count} agents")

    return jsonify({
        "status": "started",
        "task_id": task_id,
        "agent_count": agent_count,
        "message": "Agent generation started. Poll /api/simulation/status for progress."
    })


@simulation_bp.route("/start", methods=["POST"])
def start_simulation():
    """
    Launch the OASIS simulation engine.
    Body: { simulation_id, max_rounds (optional) }
    Returns: { status }
    """
    data = request.get_json()
    if not data or "simulation_id" not in data:
        return jsonify({"error": "simulation_id is required"}), 400

    max_rounds = data.get("max_rounds", 10)

    # TODO: call simulation_runner.start(simulation_id, max_rounds)

    return jsonify({
        "status": "running",
        "simulation_id": data["simulation_id"],
        "max_rounds": max_rounds,
        "message": "Simulation started."
    })


@simulation_bp.route("/pause", methods=["POST"])
def pause_simulation():
    """
    Pause the running simulation.
    Body: { simulation_id }
    """
    data = request.get_json()
    if not data or "simulation_id" not in data:
        return jsonify({"error": "simulation_id is required"}), 400

    # TODO: simulation_runner.pause(simulation_id)

    return jsonify({
        "status": "paused",
        "simulation_id": data["simulation_id"]
    })


@simulation_bp.route("/resume", methods=["POST"])
def resume_simulation():
    """
    Resume a paused simulation.
    Body: { simulation_id }
    """
    data = request.get_json()
    if not data or "simulation_id" not in data:
        return jsonify({"error": "simulation_id is required"}), 400

    # TODO: simulation_runner.resume(simulation_id)

    return jsonify({
        "status": "running",
        "simulation_id": data["simulation_id"]
    })


@simulation_bp.route("/status", methods=["GET"])
def simulation_status():
    """
    Get current simulation state.
    Query param: simulation_id
    Returns: { status, current_round, total_rounds, agent_count, elapsed_seconds }
    Status values: idle | preparing | running | paused | complete | failed
    """
    simulation_id = request.args.get("simulation_id")
    if not simulation_id:
        return jsonify({"error": "simulation_id is required"}), 400

    # TODO: return real status from simulation_runner

    return jsonify({
        "simulation_id": simulation_id,
        "status": "idle",
        "current_round": 0,
        "total_rounds": 0,
        "agent_count": 0,
        "elapsed_seconds": 0
    })


@simulation_bp.route("/feed", methods=["GET"])
def simulation_feed():
    """
    Get recent agent activity for the live feed.
    Query params: simulation_id, since_timestamp (optional), limit (optional)
    Returns: { events: [ { agent, platform, action, content, timestamp } ] }
    """
    simulation_id = request.args.get("simulation_id")
    if not simulation_id:
        return jsonify({"error": "simulation_id is required"}), 400

    since = request.args.get("since_timestamp", 0)
    limit = int(request.args.get("limit", 50))

    # TODO: load from simulation action log, filter by since_timestamp

    return jsonify({
        "simulation_id": simulation_id,
        "events": [],
        "count": 0
    })
