import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState, useMemo } from "react";
import {
  motion,
  useScroll,
  useTransform,
  useSpring,
  useMotionValue,
  useMotionTemplate,
  useAnimationFrame,
} from "motion/react";
import { Download, ArrowDown } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Porn Blocker 3.6 â€” The Final Version" },
      {
        name: "description",
        content:
          "The final, legendary release of Porn Blocker 3.6. A cinematic, once-in-a-project experience.",
      },
      { property: "og:title", content: "Porn Blocker 3.6 â€” The Final Version" },
      {
        property: "og:description",
        content: "The final, legendary release. Choose your edition.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

type Edition = {
  title: string;
  tag: string;
  hue: number;
  description: string;
  file: string;
  code: string;
};

const editions: Edition[] = [
  { title: "Porn Blocker DE 3.6", tag: "Flagship Â· Deutsch", hue: 220, description: "Beschreibung folgt.", file: "porn-blocker-de-3.6", code: "PB Â· DE 3.6" },
  { title: "Porn Blocker EN 1.6", tag: "Flagship Â· English", hue: 200, description: "Description coming soon.", file: "porn-blocker-en-1.6", code: "PB Â· EN 1.6" },
  { title: "Porn Blocker DE 3.6 Lite", tag: "Lite Â· Deutsch", hue: 180, description: "Beschreibung folgt.", file: "porn-blocker-de-3.6-lite", code: "LITE Â· DE" },
  { title: "Porn Blocker EN 1.6 Lite", tag: "Lite Â· English", hue: 160, description: "Description coming soon.", file: "porn-blocker-en-1.6-lite", code: "LITE Â· EN" },
  { title: "Porn Blocker PV Beta 0.6", tag: "Preview Â· Deutsch", hue: 280, description: "Beschreibung folgt.", file: "porn-blocker-pv-beta-0.6", code: "PV Î² Â· DE" },
  { title: "Porn Blocker EN PV Beta 0.6", tag: "Preview Â· English", hue: 300, description: "Description coming soon.", file: "porn-blocker-en-pv-beta-0.6", code: "PV Î² Â· EN" },
  { title: "Porn Blocker 3.6 Debian DE", tag: "Debian Â· Deutsch", hue: 20, description: "Beschreibung folgt.", file: "porn-blocker-3.6-debian-de", code: "DEB Â· DE" },
  { title: "Porn Blocker 1.6 Debian EN", tag: "Debian Â· English", hue: 40, description: "Description coming soon.", file: "porn-blocker-1.6-debian-en", code: "DEB Â· EN" },
  { title: "Porn Blocker Turbo EN", tag: "Turbo Â· English", hue: 340, description: "Description coming soon.", file: "porn-blocker-turbo-en", code: "TURBO Â· EN" },
  { title: "Porn Blocker Turbo DE", tag: "Turbo Â· Deutsch", hue: 0, description: "Beschreibung folgt.", file: "porn-blocker-turbo-de", code: "TURBO Â· DE" },
];

/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ STARFIELD / WARP CANVAS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
function Starfield({ boost }: { boost: React.MutableRefObject<number> }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext("2d")!;
    let raf = 0;
    let w = 0, h = 0, cx = 0, cy = 0;
    const stars: { x: number; y: number; z: number; pz: number; hue: number }[] = [];
    const N = 380;

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = window.innerWidth * dpr;
      h = canvas.height = window.innerHeight * dpr;
      canvas.style.width = window.innerWidth + "px";
      canvas.style.height = window.innerHeight + "px";
      cx = w / 2; cy = h / 2;
      ctx.scale(1, 1);
    };
    resize();
    window.addEventListener("resize", resize);

    for (let i = 0; i < N; i++) {
      stars.push({
        x: (Math.random() - 0.5) * w,
        y: (Math.random() - 0.5) * h,
        z: Math.random() * w,
        pz: 0,
        hue: 200 + Math.random() * 140,
      });
    }

    const tick = () => {
      ctx.fillStyle = "rgba(0,0,0,0.25)";
      ctx.fillRect(0, 0, w, h);
      const speed = 4 + boost.current * 40;
      for (const s of stars) {
        s.pz = s.z;
        s.z -= speed;
        if (s.z < 1) {
          s.x = (Math.random() - 0.5) * w;
          s.y = (Math.random() - 0.5) * h;
          s.z = w;
          s.pz = s.z;
        }
        const sx = (s.x / s.z) * w + cx;
        const sy = (s.y / s.z) * w + cy;
        const px = (s.x / s.pz) * w + cx;
        const py = (s.y / s.pz) * w + cy;
        const r = Math.max(0.3, (1 - s.z / w) * 2.4);
        const alpha = Math.min(1, (1 - s.z / w) * 1.2);
        ctx.strokeStyle = `hsla(${s.hue}, 90%, 70%, ${alpha})`;
        ctx.lineWidth = r;
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(sx, sy);
        ctx.stroke();
      }
      raf = requestAnimationFrame(tick);
    };
    tick();
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [boost]);

  return <canvas ref={canvasRef} className="fixed inset-0 -z-10 opacity-70" />;
}

/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ SCRAMBLE TEXT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
function useScramble(target: string, active: boolean, duration = 1400) {
  const [out, setOut] = useState(active ? target : "");
  useEffect(() => {
    if (!active) return;
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/*#@$%&";
    const start = performance.now();
    let raf = 0;
    const tick = () => {
      const t = Math.min(1, (performance.now() - start) / duration);
      const reveal = Math.floor(t * target.length);
      let s = "";
      for (let i = 0; i < target.length; i++) {
        if (i < reveal || target[i] === " ") s += target[i];
        else s += chars[Math.floor(Math.random() * chars.length)];
      }
      setOut(s);
      if (t < 1) raf = requestAnimationFrame(tick);
      else setOut(target);
    };
    tick();
    return () => cancelAnimationFrame(raf);
  }, [target, active, duration]);
  return out;
}

/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ MAIN â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
export function Index() {
  const containerRef = useRef<HTMLDivElement>(null);
  const warpBoost = useRef(0);

  const { scrollYProgress } = useScroll({ target: containerRef });
  const smooth = useSpring(scrollYProgress, { stiffness: 80, damping: 20 });

  // hero
  const heroScale = useTransform(smooth, [0, 0.25], [1, 2.6]);
  const heroOpacity = useTransform(smooth, [0, 0.18], [1, 0]);
  const heroBlur = useTransform(smooth, [0, 0.2], [0, 24]);
  const heroFilter = useMotionTemplate`blur(${heroBlur}px)`;
  const heroRotateX = useTransform(smooth, [0, 0.25], [0, -40]);

  // intro
  const introOpacity = useTransform(smooth, [0.15, 0.28, 0.45, 0.55], [0, 1, 1, 0]);
  const introY = useTransform(smooth, [0.15, 0.3], [80, 0]);
  const introScale = useTransform(smooth, [0.4, 0.55], [1, 1.2]);

  // grid
  const gridOpacity = useTransform(smooth, [0.5, 0.6], [0, 1]);
  const gridY = useTransform(smooth, [0.5, 0.62], [120, 0]);

  // bg
  const bgHue = useTransform(smooth, [0, 1], [220, 320]);
  const bgGradient = useMotionTemplate`radial-gradient(80% 60% at 50% 10%, hsl(${bgHue} 70% 18% / 0.9), transparent 60%), radial-gradient(60% 40% at 80% 80%, hsl(${bgHue} 80% 16% / 0.8), transparent 60%), #000`;

  // warp speed tied to scroll velocity
  useAnimationFrame(() => {
    const v = Math.abs((scrollYProgress as any).getVelocity?.() ?? 0);
    warpBoost.current = warpBoost.current * 0.9 + Math.min(v, 2) * 0.1;
  });

  // cursor spotlight
  const mx = useMotionValue(-500);
  const my = useMotionValue(-500);
  useEffect(() => {
    const h = (e: MouseEvent) => { mx.set(e.clientX); my.set(e.clientY); };
    window.addEventListener("pointermove", h);
    return () => window.removeEventListener("pointermove", h);
  }, [mx, my]);
  const spotlight = useMotionTemplate`radial-gradient(600px circle at ${mx}px ${my}px, hsla(280,100%,70%,0.10), transparent 40%)`;

  const heroTitle = useScramble("PORN BLOCKER", true, 1600);
  const finalTag = useScramble("FINAL RELEASE Â· MMXXVI", true, 2200);

  return (
    <div ref={containerRef} className="relative bg-black text-white" style={{ perspective: "1400px" }}>
      {/* WARP starfield */}
      <Starfield boost={warpBoost} />

      {/* Ambient background */}
      <motion.div aria-hidden className="fixed inset-0 -z-20" style={{ background: bgGradient }} />

      {/* Aurora beams */}
      <div aria-hidden className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
        <motion.div
          animate={{ rotate: [0, 360] }}
          transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
          className="absolute left-1/2 top-1/2 h-[200vmax] w-[200vmax] -translate-x-1/2 -translate-y-1/2 opacity-40"
          style={{
            background:
              "conic-gradient(from 0deg, transparent 0deg, hsla(260,90%,60%,0.25) 40deg, transparent 90deg, hsla(200,90%,60%,0.25) 200deg, transparent 260deg, hsla(320,90%,60%,0.25) 320deg, transparent 360deg)",
            filter: "blur(80px)",
          }}
        />
      </div>

      {/* Cursor spotlight */}
      <motion.div aria-hidden className="pointer-events-none fixed inset-0 z-30 mix-blend-screen" style={{ background: spotlight }} />

      {/* Grain */}
      <div aria-hidden className="pointer-events-none fixed inset-0 z-30 opacity-[0.08] mix-blend-overlay bg-[url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22160%22><filter id=%22n%22><feTurbulence baseFrequency=%220.9%22/></filter><rect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23n)%22/></svg>')]" />

      {/* Scanline vignette */}
      <div aria-hidden className="pointer-events-none fixed inset-0 z-30" style={{ boxShadow: "inset 0 0 200px 40px rgba(0,0,0,0.9)" }} />

      {/* Top HUD */}
      <div className="fixed left-6 top-6 z-40 flex items-center gap-3 text-[10px] tracking-[0.4em] text-white/50">
        <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
        LIVE Â· v3.6.FINAL
      </div>

      {/* HERO */}
      <section className="sticky top-0 flex h-screen items-center justify-center overflow-hidden">
        {/* pulsing sonar rings */}
        <div aria-hidden className="pointer-events-none absolute inset-0 flex items-center justify-center">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              initial={{ scale: 0.4, opacity: 0.6 }}
              animate={{ scale: 2.6, opacity: 0 }}
              transition={{ duration: 5, delay: i * 1.6, repeat: Infinity, ease: "easeOut" }}
              className="absolute h-[38vmin] w-[38vmin] rounded-full border border-white/20"
            />
          ))}
        </div>

        <motion.div
          style={{
            scale: heroScale,
            opacity: heroOpacity,
            filter: heroFilter,
            rotateX: heroRotateX,
            transformStyle: "preserve-3d",
          }}
          className="relative px-6 text-center"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.6, delay: 0.4 }}
            className="mb-8 font-mono text-[10px] tracking-[0.6em] text-white/50"
          >
            {finalTag}
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 60 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 2, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="relative font-mono text-[clamp(2rem,7vw,7rem)] font-semibold tracking-[0.02em] text-white/90"
          >
            <span
              className="relative inline-block"
              style={{
                textShadow:
                  "3px 0 0 rgba(255,0,180,0.35), -3px 0 0 rgba(0,180,255,0.35)",
              }}
            >
              {heroTitle}
            </span>
          </motion.h1>

          <motion.div
            initial={{ opacity: 0, scale: 0.7, filter: "blur(30px)" }}
            animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
            transition={{ duration: 2.2, delay: 1.4, ease: [0.16, 1, 0.3, 1] }}
            className="mt-2 text-[clamp(6rem,22vw,22rem)] font-thin leading-[0.85] tracking-[-0.05em]"
            style={{
              background:
                "linear-gradient(180deg, #ffffff 0%, #b8c5ff 25%, #7c93ff 55%, #ff5cf0 85%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              filter: "drop-shadow(0 0 80px rgba(124,147,255,0.55)) drop-shadow(0 0 120px rgba(255,92,240,0.35))",
            }}
          >
            3.6
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 2, delay: 2.4 }}
            className="mx-auto mt-6 max-w-xl text-lg font-light text-white/70"
          >
            The last release. The definitive edition. Everything, refined into one final chapter.
          </motion.p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 2, delay: 3 }}
            className="mt-14 flex flex-col items-center gap-2 text-[10px] tracking-[0.5em] text-white/40"
          >
            <ArrowDown className="h-3.5 w-3.5 animate-bounce" />
            SCROLL TO CONTINUE
          </motion.div>
        </motion.div>
      </section>

      {/* MARQUEE */}
      <div className="pointer-events-none relative -mt-24 overflow-hidden py-6">
        <motion.div
          animate={{ x: ["0%", "-50%"] }}
          transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
          className="flex whitespace-nowrap text-[clamp(2rem,7vw,7rem)] font-semibold tracking-tight text-white/[0.06]"
        >
          {Array.from({ length: 2 }).map((_, k) => (
            <span key={k} className="flex shrink-0 gap-16 pr-16">
              {["FINAL VERSION", "3.6", "TEN EDITIONS", "MMXXVI", "PORN BLOCKER", "FINAL RELEASE"].map((w, i) => (
                <span key={i} className="flex items-center gap-16">
                  {w}
                  <span className="text-white/[0.04]">âœ¦</span>
                </span>
              ))}
            </span>
          ))}
        </motion.div>
      </div>

      {/* INTRO */}
      <section className="relative h-[220vh]">
        <motion.div
          style={{ opacity: introOpacity, y: introY, scale: introScale }}
          className="sticky top-0 flex h-screen items-center justify-center px-6"
        >
          <div className="max-w-4xl text-center">
            <div className="mb-6 font-mono text-[10px] tracking-[0.5em] text-white/40">CHAPTER I</div>
            <h2 className="text-[clamp(2rem,5.5vw,5rem)] font-semibold leading-[1.02] tracking-tight">
              Years of work.<br />
              <span
                style={{
                  background: "linear-gradient(90deg, #7c93ff, #ff5cf0)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                One final version.
              </span>
            </h2>
            <p className="mx-auto mt-8 max-w-2xl text-lg font-light leading-relaxed text-white/60">
              Porn Blocker 3.6 is where every idea lands. Ten editions. Every platform.
              Every language that mattered. This is the version that stays.
            </p>

            {/* stat rail */}
            <div className="mx-auto mt-14 grid max-w-3xl grid-cols-3 gap-6">
              {[
                { k: "10", v: "Editions" },
                { k: "2", v: "Languages" },
                { k: "âˆž", v: "Final" },
              ].map((s) => (
                <div key={s.v} className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-6 backdrop-blur">
                  <div className="text-4xl font-thin tracking-tight">{s.k}</div>
                  <div className="mt-2 text-[10px] tracking-[0.4em] text-white/40">{s.v.toUpperCase()}</div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </section>

      {/* GRID */}
      <motion.section style={{ opacity: gridOpacity, y: gridY }} className="relative px-6 pb-40 pt-24">
        <div className="mx-auto mb-20 max-w-6xl text-center">
          <div className="mb-4 font-mono text-[10px] tracking-[0.5em] text-white/40">CHAPTER II</div>
          <h2 className="text-[clamp(2.5rem,6.5vw,5.5rem)] font-semibold leading-[1] tracking-tight">
            Choose your edition.
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-lg font-light text-white/60">
            Ten cuts of the final release. Pick the one that belongs to you.
          </p>
        </div>

        <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {editions.map((ed, i) => (
            <CubeCard key={ed.file} edition={ed} index={i} />
          ))}
        </div>

        <div className="mx-auto mt-40 max-w-3xl text-center">
          <div className="font-mono text-[10px] tracking-[0.6em] text-white/30">â—†  FIN  â—†</div>
          <p className="mt-6 text-sm font-light text-white/40">
            Porn Blocker 3.6 â€” the final version. Thank you for every version before.
          </p>
        </div>
      </motion.section>
    </div>
  );
}

/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ CUBE CARD (mouse tilt + shine sweep) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
function CubeCard({ edition, index }: { edition: Edition; index: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const rx = useMotionValue(0);
  const ry = useMotionValue(0);
  const px = useMotionValue(50);
  const py = useMotionValue(50);
  const srx = useSpring(rx, { stiffness: 180, damping: 18 });
  const sry = useSpring(ry, { stiffness: 180, damping: 18 });

  const onMove = (e: React.PointerEvent) => {
    const el = ref.current!;
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    ry.set((x - 0.5) * 18);
    rx.set(-(y - 0.5) * 18);
    px.set(x * 100);
    py.set(y * 100);
  };
  const onLeave = () => { rx.set(0); ry.set(0); };

  const shine = useMotionTemplate`radial-gradient(320px circle at ${px}% ${py}%, hsla(${edition.hue},100%,75%,0.35), transparent 60%)`;
  const border = useMotionTemplate`conic-gradient(from ${py}deg at 50% 50%, hsl(${edition.hue} 90% 65%), hsl(${edition.hue + 80} 90% 65%), hsl(${edition.hue} 90% 65%))`;

  return (
    <motion.div
      ref={ref}
      onPointerMove={onMove}
      onPointerLeave={onLeave}
      initial={{ opacity: 0, y: 80, rotateX: -25 }}
      whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 1, delay: (index % 4) * 0.08, ease: [0.16, 1, 0.3, 1] }}
      style={{
        rotateX: srx,
        rotateY: sry,
        transformStyle: "preserve-3d",
      }}
      className="group relative aspect-square"
    >
      {/* animated conic border */}
      <motion.div
        aria-hidden
        className="absolute -inset-[1px] rounded-3xl opacity-40 blur-[2px] transition-opacity duration-500 group-hover:opacity-100"
        style={{ background: border }}
      />
      <div
        className="relative flex h-full flex-col justify-between overflow-hidden rounded-3xl border border-white/10 p-6"
        style={{
          background: `linear-gradient(145deg, hsl(${edition.hue} 60% 14% / 0.95), hsl(${edition.hue + 40} 70% 6% / 0.98))`,
          boxShadow: `0 30px 60px -25px hsl(${edition.hue} 80% 30% / 0.5), inset 0 1px 0 rgba(255,255,255,0.08)`,
        }}
      >
        {/* shine following pointer */}
        <motion.div aria-hidden className="pointer-events-none absolute inset-0" style={{ background: shine }} />

        {/* glow orb */}
        <div
          aria-hidden
          className="pointer-events-none absolute -right-16 -top-16 h-52 w-52 rounded-full opacity-40 blur-3xl transition group-hover:opacity-80"
          style={{ background: `hsl(${edition.hue} 90% 55%)` }}
        />

        {/* rotating conic under */}
        <motion.div
          aria-hidden
          animate={{ rotate: 360 }}
          transition={{ duration: 24, ease: "linear", repeat: Infinity }}
          className="pointer-events-none absolute -bottom-24 -left-24 h-72 w-72 rounded-full opacity-20 blur-2xl"
          style={{ background: `conic-gradient(from 0deg, hsl(${edition.hue} 90% 60%), hsl(${edition.hue + 120} 90% 60%), hsl(${edition.hue} 90% 60%))` }}
        />

        {/* corner index */}
        <div className="absolute right-5 top-5 font-mono text-[10px] tracking-[0.3em] text-white/40">
          â„– {String(index + 1).padStart(2, "0")}
        </div>

        <div className="relative">
          <div className="text-[10px] font-medium tracking-[0.3em] text-white/50">{edition.tag}</div>
          <h3 className="mt-3 text-xl font-semibold leading-tight tracking-tight sm:text-2xl">
            {edition.title}
          </h3>
          <div className="mt-2 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-2.5 py-0.5 font-mono text-[9px] tracking-[0.2em] text-white/60">
            {edition.code}
          </div>
          <p className="mt-4 text-sm font-light leading-relaxed text-white/50">
            {edition.description}
          </p>
        </div>

        <a
          href={`${import.meta.env.BASE_URL}downloads/${edition.file}.zip`}
          download
          className="relative mt-6 inline-flex w-fit items-center gap-2 overflow-hidden rounded-full border border-white/20 bg-white/10 px-5 py-2.5 text-sm font-medium backdrop-blur-xl transition group-hover:border-white/40 group-hover:bg-white/20"
        >
          <Download className="h-4 w-4 transition group-hover:translate-y-0.5" />
          Download
          <span
            aria-hidden
            className="pointer-events-none absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/40 to-transparent transition-transform duration-1000 group-hover:translate-x-full"
          />
        </a>
      </div>
    </motion.div>
  );
}

