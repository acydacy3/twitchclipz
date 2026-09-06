import {
  AbsoluteFill, Img, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig,
  interpolate, Easing, spring, random,
} from 'remotion';

// Katastrophenprotokoll — vertikaler Motion-Shot (1080x1920) als Übungsstück.
// ECHTE Bewegung statt Ken-Burns: easeOut-Push + Crash-Zoom-Punch auf ein Beat,
// horizontaler Parallax-Drift, wortweise kinetische Caption, Film-Grain + Vignette.

const FPS = 30;
export const SHOT_DUR = 186; // ~6.2s

type W = { word: string; start: number; end: number };
const WORDS: W[] = [
  { word: 'Ein', start: 0.0, end: 0.42 },
  { word: 'Hubschrauber', start: 0.42, end: 0.94 },
  { word: 'ist', start: 0.94, end: 1.1 },
  { word: 'vorbeigekommen,', start: 1.1, end: 1.76 },
  { word: 'er', start: 2.16, end: 2.26 },
  { word: 'hat', start: 2.26, end: 2.42 },
  { word: 'ihn', start: 2.42, end: 2.52 },
  { word: 'nicht', start: 2.52, end: 2.68 },
  { word: 'gesehen', start: 2.68, end: 3.06 },
];
// Payoff-Wort "gesehen" → Crash-Zoom-Punch hier
const PUNCH = Math.round(2.72 * FPS);

const easeOut = (t: number) => Easing.out(Easing.cubic)(t);

export const ProsperiShot: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // --- Kamera: langsamer Push + Crash-Zoom-Punch + Parallax-Drift ---------
  const basePush = interpolate(frame, [0, SHOT_DUR], [1.08, 1.24], {
    easing: easeOut, extrapolateRight: 'clamp',
  });
  // kurzer Punch um PUNCH herum (dreieckiger Impuls, ~10 Frames)
  const punch = interpolate(
    frame, [PUNCH - 3, PUNCH, PUNCH + 8], [0, 0.14, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' },
  );
  const scale = basePush + punch;
  const driftX = Math.sin(frame / 47) * 14 + Math.cos(frame / 83) * 8;
  const driftY = Math.cos(frame / 61) * 9;

  // sanfter Einblendstart (kein harter Cut-in)
  const introFade = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* Bildschicht mit echter Bewegung */}
      <AbsoluteFill
        style={{
          transform: `translate(${driftX}px, ${driftY}px) scale(${scale})`,
          opacity: introFade,
        }}
      >
        <Img src={staticFile('kp/s01.jpg')}
          style={{ width, height, objectFit: 'cover' }} />
      </AbsoluteFill>

      {/* Vignette + unterer Verlauf für Caption-Lesbarkeit */}
      <AbsoluteFill style={{
        background:
          'radial-gradient(120% 90% at 50% 42%, transparent 55%, rgba(0,0,0,0.55) 100%),' +
          'linear-gradient(to top, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0) 34%)',
      }} />

      {/* Film-Grain (bewegt) */}
      <Grain />

      {/* kinetische Caption, wortweise */}
      <KineticCaption frame={frame} />

      {/* Ton: echte VO + Crash-SFX genau auf den Punch + leiser Riser drunter */}
      <Audio src={staticFile('kp/s01.mp3')} />
      <Audio src={staticFile('kp/riser.mp3')} volume={0.18} />
      <Sequence from={PUNCH - 2}>
        <Audio src={staticFile('kp/hit.mp3')} volume={0.55} />
      </Sequence>
    </AbsoluteFill>
  );
};

const KineticCaption: React.FC<{ frame: number }> = ({ frame }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{
      justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 360,
    }}>
      <div style={{
        display: 'flex', flexWrap: 'wrap', justifyContent: 'center',
        gap: '0 18px', width: 900, textAlign: 'center',
      }}>
        {WORDS.map((w, i) => {
          const startF = w.start * fps;
          const isActive = frame >= startF && frame < w.end * fps + 6;
          const appeared = frame >= startF;
          const s = spring({ frame: frame - startF, fps, config: { damping: 14, stiffness: 160 } });
          const op = interpolate(frame - startF, [0, 5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
          if (!appeared) return null;
          return (
            <span key={i} style={{
              fontFamily: 'Arial Black, Arial, sans-serif',
              fontWeight: 900, fontSize: 78, lineHeight: 1.05,
              color: isActive ? '#FFC83D' : '#fff',
              WebkitTextStroke: '3px #000',
              paintOrder: 'stroke fill',
              textShadow: '0 4px 18px rgba(0,0,0,0.6)',
              transform: `translateY(${(1 - s) * 26}px) scale(${0.7 + s * 0.3})`,
              opacity: op,
              display: 'inline-block',
            }}>{w.word}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  // 60 bewegte Körner, günstig gerendert
  const dots = new Array(70).fill(0).map((_, i) => {
    const x = random(`x${i}${Math.floor(frame / 2)}`) * 1080;
    const y = random(`y${i}${Math.floor(frame / 2)}`) * 1920;
    const o = 0.04 + random(`o${i}${frame}`) * 0.06;
    return `radial-gradient(2px 2px at ${x}px ${y}px, rgba(255,255,255,${o}), transparent)`;
  });
  return <AbsoluteFill style={{ backgroundImage: dots.join(','), mixBlendMode: 'overlay' }} />;
};
