import { useState } from "react"

import popcorn from "./assets/stickers/popcorn.png"
import ImportArchive from "./ImportArchive"
import type { TasteAnalysis } from "./ImportArchive"


type MovieDashboardProps = {
  source: "letterboxd" | "netflix"
  onBack: () => void
}


function MovieDashboard({
  source,
  onBack,
}: MovieDashboardProps) {
  const [showImport, setShowImport] = useState(false)

  const [analysis, setAnalysis] =
    useState<TasteAnalysis | null>(null)


  const sourceName =
    source === "letterboxd"
      ? "Letterboxd"
      : "Netflix"


  const handleAnalysisComplete = (
    result: TasteAnalysis
  ) => {
    setAnalysis(result)
    setShowImport(false)
  }


  /* ========================================
     DRIFT INFO
  ======================================== */

  const driftTimeline =
    analysis?.drift_timeline ?? []


  const biggestDrift =
    analysis?.summary.biggest_drift


  const smallestDrift =
    driftTimeline.length > 0
      ? driftTimeline.reduce(
          (smallest, current) =>
            current.drift < smallest.drift
              ? current
              : smallest
        )
      : null


  const averageDrift =
    driftTimeline.length > 0
      ? driftTimeline.reduce(
          (total, item) =>
            total + item.drift,
          0
        ) / driftTimeline.length
      : null


  const firstDrift =
    driftTimeline.length > 0
      ? driftTimeline[0].drift
      : null


  const lastDrift =
    driftTimeline.length > 0
      ? driftTimeline[
          driftTimeline.length - 1
        ].drift
      : null


  /* ========================================
     TREND
  ======================================== */

  let driftTrend = "—"

  let driftExplanation =
    "Import your archive to discover how your taste changes through time."


  if (
    firstDrift !== null &&
    lastDrift !== null
  ) {
    const difference =
      lastDrift - firstDrift

    if (difference < -0.03) {
      driftTrend = "Settling"

      driftExplanation =
        "Your recent taste periods are becoming more similar. Your viewing preferences appear to be settling into a more consistent direction."
    }

    else if (difference > 0.03) {
      driftTrend = "Exploring"

      driftExplanation =
        "Your recent periods show larger changes. Your taste appears to be exploring increasingly different movie styles and themes."
    }

    else {
      driftTrend = "Steady"

      driftExplanation =
        "The amount your taste changes between periods has remained relatively consistent."
    }
  }


  /* ========================================
     ARCHIVE RANGE
  ======================================== */

  const firstPeriod =
    analysis?.periods[0]

  const finalPeriod =
    analysis?.periods[
      analysis.periods.length - 1
    ]


  const archiveSpan =
    firstPeriod && finalPeriod
      ? `${formatDate(
          firstPeriod.start_date
        )} — ${formatDate(
          finalPeriod.end_date
        )}`
      : "—"


  /* ========================================
     STATS
  ======================================== */

  const stats = [
    [
      "TITLES ANALYZED",

      analysis
        ? analysis.summary.matched_films.toString()
        : "—",
    ],

    [
      "TASTE PERIODS",

      analysis
        ? analysis.summary.taste_periods.toString()
        : "—",
    ],

    [
      "BIGGEST SHIFT",

      biggestDrift
        ? `${(
            biggestDrift.drift * 100
          ).toFixed(1)}%`
        : "—",
    ],

    [
      "DRIFT TREND",

      analysis
        ? driftTrend
        : "—",
    ],
  ]


  /* ========================================
     GRAPH
  ======================================== */

  const graphWidth = 600
  const graphHeight = 220


  const driftValues =
    driftTimeline.map(
      (item) => item.drift
    )


  const maxDrift =
    driftValues.length > 0
      ? Math.max(...driftValues)
      : 0


  const graphPoints =
    driftValues.length > 0
      ? driftValues.map(
          (value, index) => {

            const x =
              driftValues.length === 1
                ? graphWidth / 2
                : (
                    index /
                    (
                      driftValues.length - 1
                    )
                  ) * graphWidth


            const normalized =
              maxDrift === 0
                ? 0
                : value / maxDrift


            const y =
              graphHeight -
              normalized * 150 -
              35


            return {
              x,
              y,
              value,
            }
          }
        )

      : []


  const polylinePoints =
    graphPoints
      .map(
        (point) =>
          `${point.x},${point.y}`
      )
      .join(" ")


  return (
    <>
      <main
        style={{
          minHeight: "100vh",
          padding:
            "35px clamp(25px, 5vw, 75px) 80px",
        }}
      >

        {/* NAV */}

        <header
          style={{
            display: "flex",
            justifyContent:
              "space-between",
            alignItems: "center",

            paddingBottom: "24px",

            borderBottom:
              "1px solid var(--border)",
          }}
        >
          <button
            type="button"
            onClick={onBack}

            style={{
              border: "none",
              background: "transparent",

              color: "var(--navy)",

              cursor: "pointer",

              fontSize: "10px",
              letterSpacing: "0.14em",
            }}
          >
            ← BACK TO ARCHIVES
          </button>


          <p
            style={{
              fontSize: "12px",
              fontWeight: 500,
              letterSpacing: "0.15em",
            }}
          >
            TASTE DRIFT
          </p>


          <span
            style={{
              fontSize: "9px",
              letterSpacing: "0.14em",
              opacity: 0.5,
            }}
          >
            {sourceName.toUpperCase()} ARCHIVE
          </span>
        </header>


        {/* HERO */}

        <section
          style={{
            position: "relative",
            padding: "70px 0 55px",
          }}
        >
          <p
            style={{
              fontSize: "10px",
              letterSpacing: "0.3em",
              opacity: 0.5,
              marginBottom: "16px",
            }}
          >
            YOUR FILM ARCHIVE
          </p>


          <h1
            style={{
              fontSize:
                "clamp(3.4rem, 6vw, 6rem)",
              lineHeight: 0.95,
            }}
          >
            Your taste,
            <br />
            through time.
          </h1>


          <p
            style={{
              maxWidth: "540px",
              fontSize: "11px",
              opacity: 0.6,
              marginTop: "27px",
            }}
          >
            Discover what defines your movie taste,
            how it changes and which genres shape
            your cinematic identity.
          </p>


          <button
            type="button"

            onClick={() =>
              setShowImport(true)
            }

            style={{
              marginTop: "30px",
              padding: "15px 22px",

              border: "none",
              borderRadius: "12px",

              background: "var(--navy)",
              color: "var(--grey-light)",

              fontSize: "9px",
              letterSpacing: "0.16em",

              cursor: "pointer",

              boxShadow:
                "0 10px 25px rgba(20,33,61,0.16)",
            }}
          >
            {analysis
              ? "ANALYZE ANOTHER ARCHIVE ↗"
              : `IMPORT ${sourceName.toUpperCase()} ARCHIVE ↗`}
          </button>


          <img
            src={popcorn}
            alt=""

            style={{
              position: "absolute",

              right: "5%",
              bottom: "20px",

              width:
                "clamp(100px, 12vw, 175px)",

              transform: "rotate(5deg)",

              filter:
                "drop-shadow(0 15px 18px rgba(20,33,61,0.13))",
            }}
          />
        </section>


        {/* TOP STATS */}

        <section
          style={{
            display: "grid",

            gridTemplateColumns:
              "repeat(auto-fit, minmax(170px, 1fr))",

            gap: "14px",

            marginBottom: "18px",
          }}
        >
          {stats.map(
            ([label, value]) => (
              <article
                key={label}

                style={{
                  minHeight: "120px",
                  padding: "22px",

                  borderRadius: "17px",

                  border:
                    "1px solid var(--border)",

                  background:
                    "rgba(238,238,235,0.75)",

                  boxShadow:
                    "var(--shadow)",
                }}
              >
                <p
                  style={{
                    fontSize: "8px",
                    letterSpacing: "0.17em",
                    opacity: 0.48,
                  }}
                >
                  {label}
                </p>

                <p
                  style={{
                    fontFamily:
                      '"Playfair Display", serif',

                    fontSize:
                      label === "DRIFT TREND"
                        ? "27px"
                        : "30px",

                    marginTop: "25px",
                  }}
                >
                  {value}
                </p>
              </article>
            )
          )}
        </section>


        {/* TASTE DNA + DRIFT */}

        <section
          style={{
            display: "grid",

            gridTemplateColumns:
              "minmax(320px, 0.9fr) minmax(450px, 2fr)",

            gap: "18px",
          }}
        >

          {/* TASTE DNA */}

          <article
            style={{
              minHeight: "440px",

              padding: "30px",

              borderRadius: "22px",

              border:
                "1px solid var(--border)",

              background:
                "rgba(238,238,235,0.75)",

              boxShadow:
                "var(--shadow)",
            }}
          >
            <p
              style={{
                fontSize: "8px",
                letterSpacing: "0.2em",
                opacity: 0.45,
              }}
            >
              01 / TASTE DNA
            </p>


            <h2
              style={{
                fontFamily:
                  '"Playfair Display", serif',

                fontSize: "31px",

                marginTop: "15px",
              }}
            >
              Your cinematic
              <br />
              fingerprint.
            </h2>


            {!analysis ? (
              <p
                style={{
                  marginTop: "35px",

                  fontSize: "11px",

                  lineHeight: 1.9,

                  opacity: 0.5,
                }}
              >
                Import your archive to discover
                the genres that define your taste.
              </p>
            ) : (
              <div
                style={{
                  marginTop: "35px",

                  display: "flex",

                  flexDirection: "column",

                  gap: "22px",
                }}
              >
                {analysis.genre_profile.map(
                  (item) => (
                    <div
                      key={item.genre}
                    >
                      <div
                        style={{
                          display: "flex",

                          justifyContent:
                            "space-between",

                          marginBottom: "8px",

                          fontSize: "10px",
                        }}
                      >
                        <span>
                          {item.genre}
                        </span>

                        <span
                          style={{
                            opacity: 0.5,
                          }}
                        >
                          {item.score.toFixed(1)}%
                        </span>
                      </div>


                      <div
                        style={{
                          width: "100%",
                          height: "5px",

                          borderRadius: "100px",

                          background:
                            "rgba(20,33,61,0.10)",

                          overflow: "hidden",
                        }}
                      >
                        <div
                          style={{
                            width:
                              `${item.score}%`,

                            height: "100%",

                            borderRadius:
                              "100px",

                            background:
                              "var(--navy)",

                            transition:
                              "width 700ms ease",
                          }}
                        />
                      </div>
                    </div>
                  )
                )}
              </div>
            )}
          </article>


          {/* DRIFT GRAPH */}

          <article
            style={{
              minHeight: "440px",

              padding: "30px",

              borderRadius: "22px",

              border:
                "1px solid var(--border)",

              background:
                "rgba(238,238,235,0.75)",

              boxShadow:
                "var(--shadow)",
            }}
          >
            <div
              style={{
                display: "flex",

                justifyContent:
                  "space-between",

                alignItems:
                  "flex-start",
              }}
            >
              <div>
                <p
                  style={{
                    fontSize: "8px",

                    letterSpacing:
                      "0.2em",

                    opacity: 0.45,
                  }}
                >
                  02 / TASTE DRIFT
                </p>


                <h2
                  style={{
                    fontFamily:
                      '"Playfair Display", serif',

                    fontSize: "31px",

                    marginTop: "15px",
                  }}
                >
                  How you've changed.
                </h2>
              </div>


              {analysis && (
                <span
                  style={{
                    fontSize: "9px",

                    letterSpacing:
                      "0.12em",

                    opacity: 0.4,
                  }}
                >
                  EMBEDDING ANALYSIS
                </span>
              )}
            </div>


            {!analysis ? (
              <div
                style={{
                  height: "245px",

                  display: "flex",

                  alignItems: "center",

                  justifyContent:
                    "center",

                  marginTop: "40px",
                }}
              >
                <p
                  style={{
                    fontSize: "9px",

                    letterSpacing:
                      "0.14em",

                    opacity: 0.35,
                  }}
                >
                  IMPORT YOUR ARCHIVE TO
                  GENERATE THE TIMELINE
                </p>
              </div>
            ) : (
              <div
                style={{
                  height: "245px",

                  marginTop: "55px",

                  borderLeft:
                    "1px solid var(--border)",

                  borderBottom:
                    "1px solid var(--border)",
                }}
              >
                <svg
                  viewBox={`0 0 ${graphWidth} ${graphHeight}`}

                  preserveAspectRatio="none"

                  style={{
                    width: "100%",
                    height: "100%",
                    overflow: "visible",
                  }}
                >
                  <polyline
                    points={polylinePoints}

                    fill="none"

                    stroke="#14213d"

                    strokeWidth="3"

                    vectorEffect=
                      "non-scaling-stroke"
                  />


                  {graphPoints.map(
                    (point, index) => (
                      <g key={index}>
                        <circle
                          cx={point.x}
                          cy={point.y}

                          r="6"

                          fill="#d8d8d5"

                          stroke="#14213d"

                          strokeWidth="3"

                          vectorEffect=
                            "non-scaling-stroke"
                        />


                        <text
                          x={point.x}

                          y={point.y - 15}

                          textAnchor="middle"

                          fill="#14213d"

                          fontSize="15"
                        >
                          {(
                            point.value * 100
                          ).toFixed(1)}
                          %
                        </text>
                      </g>
                    )
                  )}
                </svg>


                <div
                  style={{
                    display: "flex",

                    justifyContent:
                      "space-between",

                    marginTop: "13px",

                    fontSize: "8px",

                    opacity: 0.45,
                  }}
                >
                  {driftTimeline.map(
                    (item) => (
                      <span
                        key={`${item.from_period}-${item.to_period}`}
                      >
                        P{item.from_period}
                        →P{item.to_period}
                      </span>
                    )
                  )}
                </div>
              </div>
            )}
          </article>

        </section>


        {/* TASTE STORY */}

        {analysis && (
          <section
            style={{
              marginTop: "18px",

              display: "grid",

              gridTemplateColumns:
                "repeat(auto-fit, minmax(220px, 1fr))",

              gap: "14px",
            }}
          >
            <StoryCard
              label="ARCHIVE SPAN"
              value={archiveSpan}
            />

            <StoryCard
              label="BIGGEST CHANGE"

              value={
                biggestDrift
                  ? `P${biggestDrift.from_period} → P${biggestDrift.to_period}`
                  : "—"
              }

              description={
                biggestDrift
                  ? `${(
                      biggestDrift.drift *
                      100
                    ).toFixed(1)}% drift`
                  : undefined
              }
            />

            <StoryCard
              label="MOST STABLE"

              value={
                smallestDrift
                  ? `P${smallestDrift.from_period} → P${smallestDrift.to_period}`
                  : "—"
              }

              description={
                smallestDrift
                  ? `${(
                      smallestDrift.drift *
                      100
                    ).toFixed(1)}% drift`
                  : undefined
              }
            />

            <StoryCard
              label="AVERAGE CHANGE"

              value={
                averageDrift !== null
                  ? `${(
                      averageDrift * 100
                    ).toFixed(1)}%`
                  : "—"
              }
            />
          </section>
        )}


        {/* INTERPRETATION */}

        {analysis && (
          <section
            style={{
              marginTop: "18px",

              padding: "30px",

              borderRadius: "20px",

              border:
                "1px solid var(--border)",

              background:
                "rgba(238,238,235,0.66)",

              boxShadow:
                "var(--shadow)",
            }}
          >
            <p
              style={{
                fontSize: "8px",

                letterSpacing: "0.2em",

                opacity: 0.45,
              }}
            >
              03 / INTERPRETATION
            </p>


            <h2
              style={{
                fontFamily:
                  '"Playfair Display", serif',

                fontSize: "28px",

                marginTop: "13px",
              }}
            >
              Your taste is {driftTrend.toLowerCase()}.
            </h2>


            <p
              style={{
                maxWidth: "780px",

                marginTop: "13px",

                fontSize: "11px",

                lineHeight: 1.9,

                opacity: 0.6,
              }}
            >
              {driftExplanation}
            </p>
          </section>
        )}


        {/* PERIODS */}

        {analysis && (
          <section
            style={{
              marginTop: "18px",

              display: "grid",

              gridTemplateColumns:
                "repeat(auto-fit, minmax(180px, 1fr))",

              gap: "14px",
            }}
          >
            {analysis.periods.map(
              (period) => (
                <article
                  key={period.period}

                  style={{
                    padding: "20px",

                    borderRadius: "16px",

                    border:
                      "1px solid var(--border)",

                    background:
                      "rgba(238,238,235,0.6)",
                  }}
                >
                  <p
                    style={{
                      fontSize: "9px",

                      letterSpacing:
                        "0.15em",

                      opacity: 0.45,
                    }}
                  >
                    PERIOD {period.period}
                  </p>


                  <p
                    style={{
                      fontFamily:
                        '"Playfair Display", serif',

                      fontSize: "22px",

                      marginTop: "12px",
                    }}
                  >
                    {period.movies} titles
                  </p>


                  <p
                    style={{
                      fontSize: "8px",

                      opacity: 0.45,

                      marginTop: "8px",
                    }}
                  >
                    {formatDate(
                      period.start_date
                    )}

                    {" → "}

                    {formatDate(
                      period.end_date
                    )}
                  </p>
                </article>
              )
            )}
          </section>
        )}

      </main>


      {/* IMPORT */}

      {showImport && (
        <ImportArchive
          source={source}

          onClose={() =>
            setShowImport(false)
          }

          onAnalysisComplete={
            handleAnalysisComplete
          }
        />
      )}

    </>
  )
}


/* ========================================
   STORY CARD
======================================== */

function StoryCard({
  label,
  value,
  description,
}: {
  label: string
  value: string
  description?: string
}) {
  return (
    <article
      style={{
        padding: "22px",

        borderRadius: "17px",

        border:
          "1px solid var(--border)",

        background:
          "rgba(238,238,235,0.65)",
      }}
    >
      <p
        style={{
          fontSize: "8px",

          letterSpacing: "0.14em",

          opacity: 0.42,
        }}
      >
        {label}
      </p>


      <p
        style={{
          fontFamily:
            '"Playfair Display", serif',

          fontSize: "21px",

          marginTop: "8px",
        }}
      >
        {value}
      </p>


      {description && (
        <p
          style={{
            fontSize: "8px",

            opacity: 0.42,

            marginTop: "5px",
          }}
        >
          {description}
        </p>
      )}
    </article>
  )
}


/* ========================================
   DATE
======================================== */

function formatDate(
  dateString: string
) {
  const date =
    new Date(dateString)

  return date.toLocaleDateString(
    "en-US",
    {
      month: "short",
      year: "numeric",
    }
  )
}


export default MovieDashboard