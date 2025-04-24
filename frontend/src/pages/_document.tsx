import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Press+Start+2P&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=VT323&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/icon?family=Material+Icons"
        />
        <style jsx global>{`
          body {
            background-color: #F7F7F7;
            background-image: 
              linear-gradient(45deg, #FF6B6B 25%, transparent 25%),
              linear-gradient(-45deg, #FF6B6B 25%, transparent 25%),
              linear-gradient(45deg, transparent 75%, #4ECDC4 75%),
              linear-gradient(-45deg, transparent 75%, #4ECDC4 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            position: relative;
            overflow-x: hidden;
            min-height: 100vh;
          }

          body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
              0deg,
              rgba(0, 0, 0, 0.15),
              rgba(0, 0, 0, 0.15) 1px,
              transparent 1px,
              transparent 2px
            );
            pointer-events: none;
            z-index: 1;
          }

          .retro-border {
            position: relative;
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 8px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
            overflow: hidden;
          }

          .retro-border::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
              45deg,
              transparent 0%,
              rgba(255, 255, 255, 0.1) 50%,
              transparent 100%
            );
            pointer-events: none;
          }

          .pixel-text {
            font-family: 'VT323', monospace;
            letter-spacing: 1px;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.1);
          }

          .retro-button {
            position: relative;
            overflow: hidden;
            border: 2px solid #2D3436;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
          }

          .retro-button::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
              45deg,
              transparent 0%,
              rgba(255, 255, 255, 0.2) 50%,
              transparent 100%
            );
            transform: translateX(-100%);
            transition: transform 0.6s ease;
          }

          .retro-button:hover::after {
            transform: translateX(100%);
          }

          .retro-button:active {
            transform: translateY(2px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          }

          @keyframes scanline {
            0% {
              transform: translateY(-100%);
            }
            100% {
              transform: translateY(100%);
            }
          }

          .scanline {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
              to bottom,
              transparent 50%,
              rgba(0, 0, 0, 0.1) 50%
            );
            background-size: 100% 4px;
            pointer-events: none;
            animation: scanline 8s linear infinite;
            z-index: 2;
          }

          @keyframes flicker {
            0% { opacity: 1; }
            50% { opacity: 0.98; }
            100% { opacity: 1; }
          }

          .screen-flicker {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.02);
            pointer-events: none;
            animation: flicker 0.15s infinite;
            z-index: 3;
          }

          @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
          }

          .glitch-effect {
            animation: glitch 0.5s infinite;
          }

          @media (max-width: 600px) {
            .retro-border {
              border-width: 1px;
            }
            
            .retro-button {
              padding: 8px 12px;
              font-size: 0.875rem;
            }
          }

          @media (min-width: 601px) and (max-width: 900px) {
            .retro-border {
              border-width: 1px;
            }
          }

          @media (min-width: 901px) {
            .retro-border {
              border-width: 1px;
            }
          }
        `}</style>
      </Head>
      <body>
        <div className="scanline" />
        <div className="screen-flicker" />
        <Main />
        <NextScript />
      </body>
    </Html>
  );
} 