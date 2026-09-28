import { useRef, useState } from "react"


export type TasteAnalysis = {
  summary: {
    films_in_file: number
    liked_films: number
    matched_films: number
    match_rate: number
    average_rating: number
    taste_periods: number
    taste_eras: number

    biggest_drift: {
      from_period: number
      to_period: number
      similarity: number
      drift: number
    } | null
  }

  genre_profile: {
    genre: string
    score: number
  }[]

  taste_eras: {
    era: number
    cluster: number
    periods: number[]
    start_date: string
    end_date: string
  }[]

  periods: {
    period: number
    start_date: string
    end_date: string
    movies: number
  }[]

  drift_timeline: {
    from_period: number
    to_period: number
    similarity: number
    drift: number
  }[]
}


type ImportArchiveProps = {
  source: "letterboxd" | "netflix"

  onClose: () => void

  onAnalysisComplete: (
    analysis: TasteAnalysis
  ) => void
}


function ImportArchive({
  source,
  onClose,
  onAnalysisComplete,
}: ImportArchiveProps) {
  const fileInputRef =
    useRef<HTMLInputElement>(null)

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null)

  const [uploading, setUploading] =
    useState(false)

  const [message, setMessage] =
    useState("")

  const [success, setSuccess] =
    useState(false)


  const sourceName =
    source === "letterboxd"
      ? "Letterboxd"
      : "Netflix"


  const acceptedFiles =
    source === "letterboxd"
      ? ".csv,.zip"
      : ".csv"


  const handleFile = (
    file?: File
  ) => {
    if (!file) return

    setSelectedFile(file)
    setMessage("")
    setSuccess(false)
  }


  const analyzeArchive = async () => {
    if (!selectedFile) return

    setUploading(true)
    setMessage("")
    setSuccess(false)

    const formData =
      new FormData()

    formData.append(
      "source",
      source
    )

    formData.append(
      "file",
      selectedFile
    )

    try {
      const response =
        await fetch(
          "http://127.0.0.1:8000/upload-archive",
          {
            method: "POST",
            body: formData,
          }
        )

      const data =
        await response.json()


      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Analysis failed."
        )
      }


      if (
        data.analyzed &&
        data.analysis
      ) {
        setSuccess(true)

        setMessage(
          "Taste analysis complete."
        )

        setTimeout(() => {
          onAnalysisComplete(
            data.analysis
          )
        }, 600)

        return
      }


      setSuccess(true)

      setMessage(
        data.message ||
          "Archive uploaded successfully."
      )
    }

    catch (error) {
      setSuccess(false)

      if (
        error instanceof Error
      ) {
        setMessage(
          error.message
        )
      }

      else {
        setMessage(
          "Something went wrong."
        )
      }
    }

    finally {
      setUploading(false)
    }
  }


  return (
    <div
      style={{
        position: "fixed",

        inset: 0,

        zIndex: 1000,

        display: "flex",

        justifyContent:
          "center",

        alignItems:
          "center",

        padding: "25px",

        background:
          "rgba(20, 33, 61, 0.22)",

        backdropFilter:
          "blur(12px)",
      }}
    >
      <section
        style={{
          width:
            "min(600px, 100%)",

          padding: "38px",

          background:
            "var(--grey-card)",

          border:
            "1px solid var(--border)",

          borderRadius:
            "24px",

          boxShadow:
            "0 30px 80px rgba(20, 33, 61, 0.20)",
        }}
      >

        {/* HEADER */}

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
                fontSize:
                  "9px",

                letterSpacing:
                  "0.22em",

                opacity:
                  0.5,
              }}
            >
              IMPORT ARCHIVE
            </p>


            <h2
              style={{
                fontFamily:
                  '"Playfair Display", serif',

                fontSize:
                  "38px",

                marginTop:
                  "10px",
              }}
            >
              {sourceName}
            </h2>

          </div>


          <button
            type="button"

            onClick={
              onClose
            }

            style={{
              width:
                "38px",

              height:
                "38px",

              borderRadius:
                "50%",

              border:
                "1px solid var(--border)",

              background:
                "transparent",

              color:
                "var(--navy)",

              cursor:
                "pointer",

              fontSize:
                "17px",
            }}
          >
            ×
          </button>

        </div>


        {/* DESCRIPTION */}

        <p
          style={{
            fontSize:
              "11px",

            lineHeight:
              1.8,

            opacity:
              0.58,

            maxWidth:
              "470px",

            marginTop:
              "18px",
          }}
        >
          {source ===
          "letterboxd"

            ? "Upload your Letterboxd export. Taste Drift will use your movie history and ratings to analyze how your taste changes over time."

            : "Upload your Netflix viewing history. Taste Drift will analyze your watched titles and how your viewing taste changes over time."
          }
        </p>


        {/* FILE PICKER */}

        <button
          type="button"

          onClick={() =>
            fileInputRef
              .current
              ?.click()
          }

          style={{
            width:
              "100%",

            minHeight:
              "190px",

            marginTop:
              "32px",

            padding:
              "25px",

            borderRadius:
              "18px",

            border:
              "1px dashed rgba(20, 33, 61, 0.30)",

            background:
              "rgba(216, 216, 213, 0.45)",

            color:
              "var(--navy)",

            cursor:
              "pointer",

            display:
              "flex",

            flexDirection:
              "column",

            alignItems:
              "center",

            justifyContent:
              "center",
          }}
        >

          <span
            style={{
              fontFamily:
                '"Playfair Display", serif',

              fontSize:
                "34px",
            }}
          >
            +
          </span>


          <span
            style={{
              marginTop:
                "12px",

              fontSize:
                "10px",

              letterSpacing:
                "0.14em",
            }}
          >
            CHOOSE YOUR ARCHIVE
          </span>


          <span
            style={{
              marginTop:
                "8px",

              fontSize:
                "9px",

              opacity:
                0.4,
            }}
          >
            {source ===
            "letterboxd"

              ? "CSV OR LETTERBOXD EXPORT ZIP"

              : "NETFLIX VIEWING HISTORY CSV"
            }
          </span>

        </button>


        <input
          ref={
            fileInputRef
          }

          type="file"

          accept={
            acceptedFiles
          }

          hidden

          onChange={(
            event
          ) =>
            handleFile(
              event
                .target
                .files?.[0]
            )
          }
        />


        {/* SELECTED FILE */}

        {selectedFile && (

          <div
            style={{
              marginTop:
                "18px",

              padding:
                "16px 18px",

              borderRadius:
                "14px",

              border:
                "1px solid var(--border)",

              display:
                "flex",

              justifyContent:
                "space-between",

              alignItems:
                "center",
            }}
          >

            <div>

              <p
                style={{
                  fontSize:
                    "10px",

                  fontWeight:
                    500,
                }}
              >
                {
                  selectedFile.name
                }
              </p>


              <p
                style={{
                  fontSize:
                    "8px",

                  opacity:
                    0.4,

                  marginTop:
                    "5px",
                }}
              >
                {(
                  selectedFile.size /
                  1024
                ).toFixed(1)} KB
              </p>

            </div>


            <span
              style={{
                fontSize:
                  "9px",

                letterSpacing:
                  "0.12em",

                opacity:
                  0.55,
              }}
            >
              READY
            </span>

          </div>

        )}


        {/* RESULT */}

        {message && (

          <div
            style={{
              marginTop:
                "18px",

              padding:
                "13px 16px",

              borderRadius:
                "12px",

              background:
                success
                  ? "rgba(20, 33, 61, 0.08)"
                  : "rgba(120, 40, 40, 0.08)",

              fontSize:
                "9px",

              letterSpacing:
                "0.08em",
            }}
          >
            {success
              ? "✓ "
              : "⚠ "
            }

            {message}
          </div>

        )}


        {/* ANALYZE BUTTON */}

        <button
          type="button"

          disabled={
            !selectedFile ||
            uploading
          }

          onClick={
            analyzeArchive
          }

          style={{
            width:
              "100%",

            marginTop:
              "25px",

            padding:
              "17px",

            border:
              "none",

            borderRadius:
              "14px",

            background:
              selectedFile &&
              !uploading

                ? "var(--navy)"

                : "rgba(20, 33, 61, 0.12)",

            color:
              selectedFile &&
              !uploading

                ? "var(--grey-light)"

                : "rgba(20, 33, 61, 0.35)",

            cursor:
              selectedFile &&
              !uploading

                ? "pointer"

                : "default",

            fontSize:
              "10px",

            letterSpacing:
              "0.16em",

            boxShadow:
              selectedFile &&
              !uploading

                ? "0 10px 25px rgba(20,33,61,0.16)"

                : "none",
          }}
        >

          {uploading
            ? "ANALYZING YOUR TASTE..."
            : "ANALYZE MY TASTE →"
          }

        </button>


        <p
          style={{
            textAlign:
              "center",

            fontSize:
              "8px",

            letterSpacing:
              "0.1em",

            opacity:
              0.35,

            marginTop:
              "16px",
          }}
        >
          YOUR ARCHIVE IS ANALYZED USING YOUR MOVIE HISTORY
        </p>

      </section>
    </div>
  )
}


export default ImportArchive