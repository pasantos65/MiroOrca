# Credits

MiroOrca would not exist without the following open-source projects and their authors.

---

## MiroFish
**Repository:** https://github.com/666ghj/MiroFish  
**Author:** 666ghj / Shanda Group  
**Role:** The original swarm intelligence engine that MiroOrca is derived from.  
**License:** AGPL-3.0

MiroFish is a next-generation AI prediction engine powered by multi-agent technology. It introduced the core 5-stage pipeline (Graph Build → Agent Setup → Simulation → Report → Deep Interaction) that MiroOrca follows.

---

## MiroShark
**Repository:** https://github.com/aaronjmars/MiroShark  
**Author:** aaronjmars  
**Role:** English-first fork of MiroFish; introduced Neo4j as a local graph database replacement for Zep Cloud, smart model routing, and Claude Code CLI support.  
**License:** AGPL-3.0

MiroOrca's English codebase and Neo4j storage architecture are derived directly from MiroShark.

---

## MiroFish-Offline
**Repository:** https://github.com/nikmcfly/MiroFish-Offline  
**Author:** nikmcfly  
**Role:** Demonstrated the fully offline local stack (Neo4j + Ollama), which informed MiroOrca's local-first deployment approach.  
**License:** AGPL-3.0

---

## OASIS
**Repository:** https://github.com/camel-ai/oasis  
**Author:** CAMEL-AI Team  
**Role:** The multi-agent social interaction simulation engine that powers MiroOrca's simulation stage. All agent interaction, platform simulation, and action logic runs on OASIS.  
**License:** Apache 2.0

---

## License Chain

MiroOrca is licensed under AGPL-3.0, consistent with the upstream MiroFish and MiroShark licenses. Any modifications deployed as a network service must be made available as open source under the same license.
