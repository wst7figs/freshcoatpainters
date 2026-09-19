import type { Metadata } from "next";
import PageHero from "@/components/PageHero";

export const metadata: Metadata = {
  title: "Gallery | Fresh Coat Painters",
  description: "Recent interior, exterior, and cabinet refinishing projects from Fresh Coat Painters.",
};

const projects = [
  { title: "Modern Exterior Refresh", tag: "Exterior" },
  { title: "Coastal Living Room", tag: "Interior" },
  { title: "Kitchen Cabinet Refinish", tag: "Cabinets" },
  { title: "Full Home Repaint", tag: "Interior" },
  { title: "Office Suite Repaint", tag: "Commercial" },
  { title: "Craftsman Trim Detail", tag: "Exterior" },
];

export default function GalleryPage() {
  return (
    <div>
      <PageHero
        title="Recent Projects"
        subtitle="A look at some of the work we're most proud of."
      />
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((p) => (
            <div key={p.title} className="overflow-hidden rounded-xl border border-zinc-200">
              <div className="flex h-48 items-center justify-center bg-gradient-to-br from-brand/10 to-accent/10">
                <span className="text-sm font-medium text-zinc-400">Photo coming soon</span>
              </div>
              <div className="p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-brand">{p.tag}</p>
                <h3 className="mt-1 font-semibold text-zinc-900">{p.title}</h3>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
