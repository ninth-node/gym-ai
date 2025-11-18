export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-6xl font-bold bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent mb-6">
          AI Gym Management
        </h1>
        <p className="text-2xl text-muted-foreground mb-8">
          The First AI-Powered Platform That Thinks Before You Do
        </p>
        <div className="flex gap-4 justify-center">
          <button className="bg-primary text-primary-foreground px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition">
            Start Your AI Transformation
          </button>
          <button className="bg-secondary text-secondary-foreground px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition">
            See Live Demo
          </button>
        </div>
      </div>
    </main>
  );
}
