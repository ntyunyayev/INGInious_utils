#!/bin/bash

COURSE_FOLDER=$1
# Base start date (Feb 5th)
START="2026-02-08"

exercises=(
    "S1 - Introduction Assembleur"
    "S2 - Assembleur: Conditions & Boucles"
    "S3 - Assembleur: Tableaux & Chaînes de charactères"
    "S4 - Assembleur: Fonctions & Procédures"
    "S5 - Assembleur: Fonctions avancées"
    "S7 - Circuits Logiques: Introduction"
    "Semaine 7 - Circuits Logiques: Circuits de base"
    "Semaine 8 - Circuits Logiques: Mémoire"
)


gaps=(2 1 1 1 1 1 1 1)
TOTAL_WEEKS=0

for i in "${!exercises[@]}"; do
    TOTAL_WEEKS=$((TOTAL_WEEKS + ${gaps[$i]}))
    
    DEADLINE=$(date -d "$START + $TOTAL_WEEKS weeks" +"%Y-%m-%d")

    DEADLINE_ARG="//$DEADLINE 23:59:59"

    echo "Updating ${exercises[$i]}..."
    python3 change_deadline.py --course_folder "$COURSE_FOLDER" --series_title "${exercises[$i]}" --new_deadline "$DEADLINE_ARG"
done
