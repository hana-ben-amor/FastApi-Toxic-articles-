import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from app.analyze_stats import compute_stats

def generate_graphs():
    stats = compute_stats()
    if stats is None:
        return

    # ======================
    # 1️⃣ Graphique à barres empilées
    # ======================
    stats.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="coolwarm")
    plt.title("Répartition des textes toxiques par site")
    plt.ylabel("Pourcentage (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("toxicite_barres.png")
    plt.close()

    # ======================
    # 2️⃣ Heatmap (carte de chaleur)
    # ======================
    plt.figure(figsize=(10, 6))
    sns.heatmap(stats, annot=True, cmap="coolwarm", fmt=".1f")
    plt.title("Heatmap - Pourcentage de toxicité par site")
    plt.savefig("toxicite_heatmap.png")
    plt.close()

    # ======================
    # 3️⃣ Graphique en lignes
    # ======================
    stats.plot(kind="line", marker="o", figsize=(10, 6))
    plt.title("Évolution des niveaux de toxicité par site")
    plt.ylabel("Pourcentage (%)")
    plt.xticks(rotation=45)
    plt.legend(title="Niveau de toxicité")
    plt.tight_layout()
    plt.savefig("toxicite_lignes.png")
    plt.close()

    # ======================
    # 4️⃣ Camembert par site
    # ======================
    for site, row in stats.iterrows():
        row.plot(kind="pie", autopct='%1.1f%%', figsize=(6, 6))
        plt.title(f"Toxicité - {site}")
        plt.ylabel("")
        plt.savefig(f"toxicite_{site}.png")
        plt.close()

    # ======================
    # 5️⃣ Boxplot pour comparer la distribution
    # ======================
    stats_melted = stats.reset_index().melt(id_vars="source", var_name="niveau", value_name="pct")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=stats_melted, x="niveau", y="pct", palette="Set2")
    plt.title("Distribution des pourcentages de toxicité par niveau")
    plt.savefig("toxicite_boxplot.png")
    plt.close()

    print("✅ Tous les graphiques (barres, heatmap, lignes, camemberts, boxplot) générés et sauvegardés (PNG).")

if __name__ == "__main__":
    generate_graphs()
