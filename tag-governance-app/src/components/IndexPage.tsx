import { motion } from "framer-motion";

const fadeUp = {
  hidden: { opacity: 0, y: 40 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.2, duration: 0.8, ease: "easeOut" },
  }),
};

export default function IndexPage() {
  return (
    <div className="bg-gradient-to-br from-gray-900 via-black to-gray-950 text-white">
      {/* Hero */}
      <section className="h-screen flex flex-col justify-center items-center text-center px-8">
        <motion.h1
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-6xl font-extrabold tracking-tight"
        >
          Tag Governance & HLJ Pipeline
        </motion.h1>
        <motion.p
          initial="hidden"
          animate="visible"
          variants={fadeUp}
          custom={1}
          className="mt-6 text-xl text-gray-300 max-w-3xl"
        >
          Central README for the research repo tying together HLJ parsing,
          versioned tag-governance, benchmarking, and the paper.
        </motion.p>
        <motion.a
          href="https://example.com/paper.pdf"
          target="_blank"
          whileHover={{ scale: 1.1, boxShadow: "0px 0px 20px rgba(168,85,247,0.6)" }}
          whileTap={{ scale: 0.95 }}
          className="mt-10 px-8 py-4 bg-purple-600 hover:bg-purple-500 rounded-lg font-semibold text-white shadow-lg transition"
        >
          📄 Read the Paper
        </motion.a>
      </section>

      {/* Why this Repo */}
      <section className="py-22 px-8 max-w-5xl mx-auto">
        <motion.h2
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="text-4xl font-bold mb-8 text-center"
        >
          Why this repo exists
        </motion.h2>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="p-8 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl shadow-lg"
        >
          <p className="text-gray-300 leading-relaxed">
            We automate requirements engineering artifacts into{" "}
            <b>High-Level JSON (HLJ)</b> and apply a{" "}
            <b>versioned tag-governance pipeline</b> (v0 → v1 → v2). The design emphasizes{" "}
            <b>auditability</b>, <b>confidence scoring</b>, and <b>reproducibility</b> across
            multi-model outputs (GPT-4.1, Opus4, Meta-70B, etc.).
          </p>
        </motion.div>
      </section>

      {/* Repo Map */}
      <section className="py-24 px-8 max-w-6xl mx-auto">
        <motion.h2
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="text-4xl font-bold mb-12 text-center"
        >
          Repo map (what lives where)
        </motion.h2>
        <div className="grid md:grid-cols-2 gap-8">
          {[
            { title: "configs/", desc: "Versioned, YAML-driven pipeline configs." },
            { title: "scripts/", desc: "Runnable modules: step_1 (eval), step_2 (governance)." },
            { title: "raw_requirement/", desc: "Domain folders with raw requirement markdown." },
            { title: "prompts/", desc: "Prompt templates for HLJ parsing and SBERT fallback prompts." },
            { title: "eval/", desc: "All evaluation artifacts: runs/<vX>, logging/, metrics." },
            { title: "output/", desc: "Model outputs under output/<model>/req-XXX." },
            { title: "docs/", desc: "In-depth docs per pipeline version." },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              custom={i}
              whileHover={{ scale: 1.05, boxShadow: "0px 0px 25px rgba(255,255,255,0.15)" }}
              className="p-6 bg-white/10 border border-white/20 rounded-lg shadow-md"
            >
              <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
              <p className="text-gray-300 text-sm">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Dataset Facts */}
      <section className="py-24 px-8 bg-black/40">
        <motion.h2
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="text-4xl font-bold mb-12 text-center"
        >
          Dataset Facts
        </motion.h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {[
            "30 real-world requirements across FinTech & SaaS.",
            "Precomputed HLJ results from GPT-4.1, Opus4, Meta-70B.",
            "Multiple run options, most efficient via README commands.",
            "Original runs/results compiled inside sbert_fix/ folder.",
          ].map((fact, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.2, duration: 0.6 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.05, borderColor: "rgba(168,85,247,0.6)" }}
              className="p-6 bg-white/5 border border-purple-500/40 rounded-lg shadow-md text-gray-300"
            >
              {fact}
            </motion.div>
          ))}
        </div>
      </section>

      {/* Runner Commands */}
      <section className="py-24 px-8 bg-black/60">
        <motion.h2
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="text-4xl font-bold mb-10 text-center"
        >
          Runner Commands
        </motion.h2>
        <div className="space-y-4 max-w-3xl mx-auto">
          {[
            "python -m scripts.run_pipeline --config configs/pipeline_v2.yaml --list",
            "python -m scripts.run_pipeline --config configs/pipeline_v2.yaml",
            "python -m scripts.run_pipeline --config configs/pipeline_v2.yaml --step detect_tag_drift.py",
          ].map((cmd, i) => (
            <motion.pre
              key={i}
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.2, duration: 0.6 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.03, backgroundColor: "rgba(88,28,135,0.3)" }}
              className="bg-black/80 border border-purple-500/40 p-4 rounded-lg text-purple-300 font-mono text-sm overflow-x-auto shadow-lg"
            >
              {cmd}
            </motion.pre>
          ))}
        </div>
      </section>

      {/* Troubleshooting */}
      <section className="py-24 px-8 max-w-4xl mx-auto">
        <motion.h2
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="text-4xl font-bold mb-8 text-center"
        >
          Troubleshooting
        </motion.h2>
        <motion.ul
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="space-y-4 text-white list-disc list-inside"
        >
          {[
            "Drift detector wants old CTD → fix prev_ctd_path.",
            "spaCy not found → python -m spacy download en_core_web_sm.",
            "SentenceTransformers issues → pre-cache models.",
          ].map((tip, i) => (
            <motion.li key={i} variants={fadeUp} custom={i} />
          ))}
        </motion.ul>
      </section>

      {/* Footer */}
      <footer className="h-32 flex justify-center items-center bg-black/90 border-t border-white/20">
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="text-gray-400 text-sm"
        >
          © 2025 Tag Governance Dataset · Built by Dvip Patel
        </motion.p>
      </footer>
    </div>
  );
}
