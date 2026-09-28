import numpy as np

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# =========================================================
# FIND BEST NUMBER OF CLUSTERS
# =========================================================

def choose_cluster_count(
    vectors,
    max_clusters=3,
):
    """
    Automatically choose a reasonable number
    of taste clusters using silhouette score.
    """

    count = len(vectors)

    if count < 3:
        return 1

    best_k = 2
    best_score = -1

    upper_limit = min(
        max_clusters,
        count - 1,
    )

    for k in range(
        2,
        upper_limit + 1,
    ):
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20,
        )

        labels = model.fit_predict(
            vectors
        )

        # Silhouette cannot work if
        # every point becomes its own cluster.
        if len(set(labels)) < 2:
            continue

        score = silhouette_score(
            vectors,
            labels,
            metric="cosine",
        )

        if score > best_score:
            best_score = score
            best_k = k

    return best_k


# =========================================================
# BUILD TASTE ERAS
# =========================================================

def detect_taste_eras(
    period_vectors,
    period_information,
):
    """
    period_vectors format:

    [
        (0, vector),
        (1, vector),
        (2, vector),
        ...
    ]

    period_information contains:
    period, start_date, end_date, movies
    """

    if not period_vectors:
        return []


    # -----------------------------------------
    # EXTRACT 384D VECTORS
    # -----------------------------------------

    vectors = np.array(
        [
            vector
            for _, vector
            in period_vectors
        ]
    )


    # -----------------------------------------
    # VERY SMALL HISTORY
    # -----------------------------------------

    if len(vectors) < 3:
        return [
            {
                "era": 1,
                "cluster": 0,
                "periods": [
                    info["period"]
                    for info
                    in period_information
                ],
                "start_date":
                    period_information[0][
                        "start_date"
                    ],
                "end_date":
                    period_information[-1][
                        "end_date"
                    ],
            }
        ]


    # -----------------------------------------
    # CHOOSE K
    # -----------------------------------------

    cluster_count = (
        choose_cluster_count(
            vectors
        )
    )


    # -----------------------------------------
    # K-MEANS
    # -----------------------------------------

    model = KMeans(
        n_clusters=cluster_count,
        random_state=42,
        n_init=20,
    )

    labels = model.fit_predict(
        vectors
    )


    # -----------------------------------------
    # TURN CLUSTERS INTO CHRONOLOGICAL ERAS
    # -----------------------------------------

    eras = []

    current_era = None

    for index, label in enumerate(
        labels
    ):
        info = (
            period_information[index]
        )

        # New taste state appeared.
        if (
            current_era is None
            or current_era["cluster"]
            != int(label)
        ):
            current_era = {
                "era":
                    len(eras) + 1,

                "cluster":
                    int(label),

                "periods": [
                    info["period"]
                ],

                "start_date":
                    info["start_date"],

                "end_date":
                    info["end_date"],
            }

            eras.append(
                current_era
            )

        else:
            current_era[
                "periods"
            ].append(
                info["period"]
            )

            current_era[
                "end_date"
            ] = info[
                "end_date"
            ]


    return eras