# Test Hardening: Claude Runbook

> Cover the error paths, configuration checks and uncalled methods a coverage run found untested, and roll back a rename whose source delete fails.
>
> **Branch:** `test-hardening` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step 1 — Hardening tests ← NEW in this branch

```bash
# fill in once the work item has tests
```

**Expected:** <runtime, pass/fail expectations, which tests are active>

### Step 2 — Coverage measurement

JaCoCo isn't in the pom, so attach it from the command line. The plugin's code inside the Trino container is counted only through a temporary `src/test/docker/docker-compose.override.yml`, which Compose picks up automatically; delete it afterwards.

```bash
mvn clean package -DskipTests
mkdir -p target/jacoco && chmod 777 target/jacoco
mvn dependency:copy -Dartifact=org.jacoco:org.jacoco.agent:0.8.15:jar:runtime -DoutputDirectory=target/jacoco
mvn dependency:copy -Dartifact=org.jacoco:org.jacoco.cli:0.8.15:jar:nodeps -DoutputDirectory=target/jacoco
mv target/jacoco/org.jacoco.agent-0.8.15-runtime.jar target/jacoco/jacocoagent.jar
mv target/jacoco/org.jacoco.cli-0.8.15-nodeps.jar target/jacoco/jacococli.jar
cat > src/test/docker/docker-compose.override.yml <<'YML'
services:
  trino:
    environment:
      JAVA_TOOL_OPTIONS: "-javaagent:/jacoco/jacocoagent.jar=destfile=/jacoco/trino.exec,append=true,includes=com.github.robfromboulder.*"
    volumes:
      - ${PROJECT_ROOT}/target/jacoco:/jacoco
YML
mvn org.jacoco:jacoco-maven-plugin:0.8.15:prepare-agent test -Djacoco.destFile=$PWD/target/jacoco/unit.exec
mvn org.jacoco:jacoco-maven-plugin:0.8.15:prepare-agent test -Pintegration -Djacoco.destFile=$PWD/target/jacoco/it.exec
rm src/test/docker/docker-compose.override.yml
cd target/jacoco && java -jar jacococli.jar report unit.exec it.exec trino.exec --classfiles ../classes --sourcefiles ../../src/main/java --html html --xml all.xml
```

**Expected:** `trino.exec` exists, which shows the container agent loaded. The baseline before this item was 92% of lines and 93% of branches.
