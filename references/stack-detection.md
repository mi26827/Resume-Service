# Technology stack detection

Triangulate four layers: **declaration** (manifest/lockfile), **implementation** (imports and symbols), **wiring** (configuration/DI/routes), and **operation** (deployment/CI/runtime artifacts). A manifest alone is `detected`; implementation plus wiring can be `used`.

| Ecosystem | Primary signals | Common framework confirmation |
|---|---|---|
| Java/Kotlin | `pom.xml`, Gradle files, source extensions | Spring annotations/config, Ktor routes, persistence clients |
| Go | `go.mod`, `go.sum`, `cmd/`, `internal/` | Gin/Fiber/Kratos/go-zero imports plus router/bootstrap |
| Python | `pyproject.toml`, requirements/Pip files | FastAPI/Django/Flask declarations plus app/URL wiring |
| JS/TS | `package.json`, lockfiles, `tsconfig.json` | Nest modules/controllers or Express/Koa router registration |
| Rust | `Cargo.toml`, lockfile | Axum/Actix dependencies plus route/server construction |
| C# | `*.csproj`, solution files | ASP.NET hosting, controller/minimal API registration |
| Ruby | `Gemfile`, Rails configuration | routes, controllers, ActiveRecord models |
| PHP | `composer.json` | Laravel routes/providers/Eloquent or framework bootstrap |

Also inspect Dockerfiles, Compose, Kubernetes, Helm, Terraform, CI/CD, migrations, generated clients, and configuration for database, cache, messaging, RPC, search, scheduler, discovery, gateway, auth, observability, containers, orchestration, cloud, and AI frameworks.

For every item record: technology/category, version if explicit, evidence locations, status (`DECLARED`, `WIRED`, `RUNTIME_FLOW`), project-specific role, and confidence. Do not infer a database from an ORM alone or a cloud from a generic SDK.
