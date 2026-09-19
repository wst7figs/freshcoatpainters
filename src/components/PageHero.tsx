export default function PageHero({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <section className="bg-gradient-to-b from-brand-dark to-brand text-white">
      <div className="mx-auto max-w-6xl px-6 py-16 text-center">
        <h1 className="text-4xl font-bold">{title}</h1>
        <p className="mx-auto mt-3 max-w-2xl text-blue-100">{subtitle}</p>
      </div>
    </section>
  );
}
