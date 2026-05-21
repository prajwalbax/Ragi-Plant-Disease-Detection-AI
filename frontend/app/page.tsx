"use client";

import { motion } from "framer-motion";
import { Activity, BrainCircuit, Leaf, ShieldCheck, Sparkles, UploadCloud } from "lucide-react";
import { HealthIndicator } from "@/components/health-indicator";
import { PredictionPanel } from "@/components/prediction-panel";

const features = [
  { icon: UploadCloud, title: "Upload leaf image", copy: "Drop a clear ragi leaf photo and let the model prepare it for inference." },
  { icon: Sparkles, title: "Instant prediction", copy: "FastAPI serves TensorFlow predictions through a clean image API." },
  { icon: Activity, title: "Confidence score", copy: "Each result includes model confidence for quick triage." },
  { icon: ShieldCheck, title: "Disease information", copy: "Readable disease context is returned with every diagnosis." },
];

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-mesh">
      <section className="mx-auto flex w-full max-w-7xl flex-col gap-10 px-4 py-6 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between rounded-none border-b border-white/10 pb-5">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg border border-primary/30 bg-primary/10">
              <Leaf className="h-5 w-5 text-primary" />
            </div>
            <span className="text-sm font-semibold uppercase tracking-[0.28em] text-primary">Ragi AI</span>
          </div>
          <HealthIndicator />
        </nav>

        <div className="grid items-center gap-10 lg:grid-cols-[0.95fr_1.05fr]">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-7 py-4"
          >
            <div 
            className="inline-flex items-center rounded-full border border-accent/30 bg-accent/10 text-accent"
            style={{ padding: '12px 24px', gap: '12px', fontSize: '1.25rem', fontWeight: '600' }}
            >
              <BrainCircuit style={{ width: '24px', height: '24px' }} />
              <span>ತಿನ್ನಿ ರಾಗಿ, ಆಗಿ ನಿರೋಗಿ.</span>
            </div>
            <div className="space-y-5">
              <h1 className="max-w-4xl text-5xl font-semibold leading-tight text-foreground sm:text-6xl lg:text-7xl">
                Ragi Disease Detection
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-muted sm:text-xl">
                World's first disease detection for finger millet (Ragi)
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {features.map((feature) => (
                <div
                  key={feature.title}
                  className="rounded-lg border border-white/10 bg-card p-4 shadow-glow backdrop-blur-xl"
                >
                  <feature.icon className="mb-3 h-5 w-5 text-primary" />
                  <h2 className="text-base font-semibold text-foreground">{feature.title}</h2>
                  <p className="mt-2 text-sm leading-6 text-muted">{feature.copy}</p>
                </div>
              ))}
            </div>
          </motion.div>

          <PredictionPanel />
        </div>
      </section>
    </main>
  );
}
