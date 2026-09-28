import { useState } from "react"
import "./transition.css"

import clapperboard from "./assets/stickers/clapperboard.png"
import MovieDashboard from "./MovieDashboard"

type MediaSource = "letterboxd" | "netflix"

const mediaTypes = [
  {
    id: "letterboxd" as MediaSource,
    number: "01",
    name: "Letterboxd",
    subtitle: "Trace the films that shaped your taste.",
  },
  {
    id: "netflix" as MediaSource,
    number: "02",
    name: "Netflix",
    subtitle: "Rediscover how your viewing habits changed over time.",
  },
]

function App() {
  const [hoveredCard, setHoveredCard] =
    useState<string | null>(null)

  const [transitioning, setTransitioning] =
    useState(false)

  const [selectedMedia, setSelectedMedia] =
    useState<MediaSource | null>(null)

  const [dashboardOpen, setDashboardOpen] =
    useState(false)

  const openMedia = (source: MediaSource) => {
    setSelectedMedia(source)
    setTransitioning(true)

    setTimeout(() => {
      setDashboardOpen(true)
      setTransitioning(false)
    }, 1500)
  }

  const goHome = () => {
    setDashboardOpen(false)
    setSelectedMedia(null)
  }

  if (dashboardOpen && selectedMedia) {
    return (
      <MovieDashboard
        source={selectedMedia}
        onBack={goHome}
      />
    )
  }

  return (
    <>
      <main
        style={{
          minHeight: "100vh",
          padding: "55px clamp(24px, 8vw, 150px) 70px",
        }}
      >
        <header
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "80px",
          }}
        >
          <p
            style={{
              fontSize: "13px",
              fontWeight: 500,
              letterSpacing: "0.08em",
            }}
          >
            TASTE DRIFT
          </p>

          <p
            style={{
              fontSize: "11px",
              opacity: 0.55,
              letterSpacing: "0.12em",
            }}
          >
            YOUR TASTE • THROUGH TIME
          </p>
        </header>

        <section
          style={{
            maxWidth: "850px",
            marginBottom: "65px",
          }}
        >
          <p
            style={{
              fontSize: "11px",
              letterSpacing: "0.25em",
              marginBottom: "18px",
              opacity: 0.65,
            }}
          >
            BEGIN YOUR ARCHIVE
          </p>

          <h1
            style={{
              fontSize: "clamp(3.5rem, 7vw, 6.8rem)",
              lineHeight: 0.95,
            }}
          >
            What shaped
            <br />
            your taste?
          </h1>

          <p
            style={{
              maxWidth: "580px",
              marginTop: "30px",
              fontSize: "13px",
              opacity: 0.65,
            }}
          >
            Choose your film archive and discover how your
            preferences changed over time.
          </p>
        </section>

        <section
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(2, minmax(280px, 1fr))",
            gap: "22px",
            maxWidth: "1000px",
          }}
        >
          {mediaTypes.map((media) => {
            const isHovered =
              hoveredCard === media.id

            return (
              <button
                key={media.id}
                type="button"
                onClick={() =>
                  openMedia(media.id)
                }
                onMouseEnter={() =>
                  setHoveredCard(media.id)
                }
                onMouseLeave={() =>
                  setHoveredCard(null)
                }
                style={{
                  position: "relative",

                  minHeight: "320px",
                  padding: "32px",

                  borderRadius: "22px",
                  border:
                    "1px solid var(--border)",

                  background: isHovered
                    ? "var(--navy)"
                    : "rgba(238,238,235,0.72)",

                  color: isHovered
                    ? "var(--grey-light)"
                    : "var(--navy)",

                  boxShadow: isHovered
                    ? "var(--shadow-hover)"
                    : "var(--shadow)",

                  transform: isHovered
                    ? "translateY(-8px)"
                    : "translateY(0)",

                  transition: "300ms ease",

                  cursor: "pointer",
                  textAlign: "left",

                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                }}
              >
                <span
                  style={{
                    fontSize: "11px",
                    letterSpacing: "0.15em",
                    opacity: 0.6,
                  }}
                >
                  {media.number}
                </span>

                <div>
                  <h2
                    style={{
                      fontFamily:
                        '"Playfair Display", serif',

                      fontSize: "38px",
                      color: "inherit",
                      marginBottom: "12px",
                    }}
                  >
                    {media.name}
                  </h2>

                  <p
                    style={{
                      fontSize: "11px",
                      maxWidth: "270px",
                      opacity: 0.68,
                    }}
                  >
                    {media.subtitle}
                  </p>
                </div>

                <span
                  style={{
                    position: "absolute",
                    right: "30px",
                    bottom: "28px",
                    fontSize: "24px",
                  }}
                >
                  ↗
                </span>
              </button>
            )
          })}
        </section>
      </main>

      {transitioning && (
        <div className="movie-transition">
          <div className="transition-content">
            <img
              src={clapperboard}
              className="transition-clapperboard"
              alt="Movie clapperboard"
            />

            <p className="transition-small-text">
              {selectedMedia === "netflix"
                ? "OPENING NETFLIX ARCHIVE"
                : "OPENING LETTERBOXD ARCHIVE"}
            </p>

            <h2 className="transition-title">
              Your Film Archive
            </h2>
          </div>
        </div>
      )}
    </>
  )
}

export default App