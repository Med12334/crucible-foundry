//! Crucible-Foundry Layers 21 to 26 (Memory-Safe Rust Execution Jailer):
//! - Classifies multi-language sandbox execution telemetry (Time Limit Exceeded,
//!   Out-Of-Memory RSS breach, forbidden syscall trap, or clean zero exit).
//! - Computes Mutation Testing Adequacy Score to verify whether AI-generated unit tests
//!   actually catch injected semantic mutants.

#[derive(Debug, Clone, PartialEq)]
pub enum SandboxVerdict {
    ExecutionPassedOptimal,
    TimeLimitExceeded,
    MemoryQuotaExceeded,
    RuntimeCrashOrSignal(i32),
}

#[derive(Debug, Clone)]
pub struct ProcessExecutionTelemetry {
    pub language_runtime: String,
    pub wall_time_ms: u64,
    pub max_wall_time_ms: u64,
    pub peak_rss_kb: u64,
    pub max_rss_kb: u64,
    pub exit_code: i32,
}

pub fn evaluate_sandbox_execution(telemetry: &ProcessExecutionTelemetry) -> SandboxVerdict {
    if telemetry.wall_time_ms > telemetry.max_wall_time_ms {
        return SandboxVerdict::TimeLimitExceeded;
    }
    if telemetry.peak_rss_kb > telemetry.max_rss_kb {
        return SandboxVerdict::MemoryQuotaExceeded;
    }
    if telemetry.exit_code != 0 {
        return SandboxVerdict::RuntimeCrashOrSignal(telemetry.exit_code);
    }
    SandboxVerdict::ExecutionPassedOptimal
}

/// Evaluates the quality of AI-generated test suites by measuring killed vs. surviving code mutants.
pub fn compute_mutation_kill_ratio(killed_mutants: u32, total_mutants: u32) -> f64 {
    if total_mutants == 0 {
        return 0.0;
    }
    let ratio = (killed_mutants as f64) / (total_mutants as f64);
    (ratio * 10000.0).round() / 10000.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sandbox_warden_enforces_time_and_memory_quotas() {
        let optimal = ProcessExecutionTelemetry {
            language_runtime: String::from("python3.11"),
            wall_time_ms: 42,
            max_wall_time_ms: 2000,
            peak_rss_kb: 18_400,
            max_rss_kb: 262_144,
            exit_code: 0,
        };
        assert_eq!(evaluate_sandbox_execution(&optimal), SandboxVerdict::ExecutionPassedOptimal);

        let oom = ProcessExecutionTelemetry {
            language_runtime: String::from("cpp20"),
            wall_time_ms: 120,
            max_wall_time_ms: 2000,
            peak_rss_kb: 512_000,
            max_rss_kb: 262_144,
            exit_code: 0,
        };
        assert_eq!(evaluate_sandbox_execution(&oom), SandboxVerdict::MemoryQuotaExceeded);
    }

    #[test]
    fn test_mutation_testing_kill_ratio_calculation() {
        assert_eq!(compute_mutation_kill_ratio(48, 50), 0.96);
        assert_eq!(compute_mutation_kill_ratio(0, 0), 0.0);
    }
}
