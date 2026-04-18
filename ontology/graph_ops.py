from __future__ import annotations

from collections import defaultdict


def build_alias_index(ontology: dict) -> dict[str, str]:
    alias_index: dict[str, str] = {}
    for concept in ontology.get("concepts", []):
        concept_id = concept["id"]
        alias_index[concept_id.lower()] = concept_id
        for alias in concept.get("aliases", []):
            alias_index[alias.lower()] = concept_id
    return alias_index


def build_adjacency(ontology: dict) -> dict[str, set[str]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for relation in ontology.get("relations", []):
        source = relation["source"]
        target = relation["target"]
        adjacency[source].add(target)
        adjacency[target].add(source)
    return adjacency


def extract_concepts(text: str, ontology: dict) -> list[str]:
    lowered = text.lower()
    alias_index = build_alias_index(ontology)
    hits: list[str] = []
    for alias, concept_id in alias_index.items():
        if alias in lowered and concept_id not in hits:
            hits.append(concept_id)
    return hits


def relation_validity_ratio(concepts: list[str], ontology: dict) -> float:
    if len(concepts) <= 1:
        return 1.0 if concepts else 0.0
    adjacency = build_adjacency(ontology)
    valid_pairs = 0
    total_pairs = 0
    for idx, source in enumerate(concepts):
        for target in concepts[idx + 1 :]:
            total_pairs += 1
            if target in adjacency.get(source, set()):
                valid_pairs += 1
    if total_pairs == 0:
        return 0.0
    return valid_pairs / total_pairs

