use serde::{Deserialize, Serialize};

/// Versioned durable assignment state owned by one engine profile.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AssignmentRecord {
    pub id: String,
    pub owner_device_id: String,
    pub profile_id: String,
    pub revision: u64,
    pub objective: String,
    pub allowed_actions: Vec<String>,
    pub linked_sessions: Vec<String>,
    pub findings: Vec<String>,
    pub evidence: Vec<String>,
    pub reviews: Vec<AssignmentReview>,
    pub unresolved_questions: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AssignmentReview {
    pub revision: u64,
    pub reviewer: String,
    pub outcome: String,
    pub notes: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CreateAssignmentRequest {
    pub id: String,
    pub objective: String,
    #[serde(default)]
    pub allowed_actions: Vec<String>,
    #[serde(default)]
    pub linked_sessions: Vec<String>,
    #[serde(default)]
    pub findings: Vec<String>,
    #[serde(default)]
    pub evidence: Vec<String>,
    #[serde(default)]
    pub reviews: Vec<AssignmentReview>,
    #[serde(default)]
    pub unresolved_questions: Vec<String>,
    #[serde(default)]
    pub owner_device_id: Option<String>,
    #[serde(default)]
    pub profile_id: Option<String>,
    pub mutation_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AssignmentMutationRequest {
    pub id: String,
    pub expected_revision: u64,
    pub mutation_id: String,
    pub objective: String,
    #[serde(default)]
    pub allowed_actions: Vec<String>,
    #[serde(default)]
    pub linked_sessions: Vec<String>,
    #[serde(default)]
    pub findings: Vec<String>,
    #[serde(default)]
    pub evidence: Vec<String>,
    #[serde(default)]
    pub reviews: Vec<AssignmentReview>,
    #[serde(default)]
    pub unresolved_questions: Vec<String>,
    #[serde(default)]
    pub owner_device_id: Option<String>,
    #[serde(default)]
    pub profile_id: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AssignmentIdRequest {
    pub id: String,
    #[serde(default)]
    pub owner_device_id: Option<String>,
    #[serde(default)]
    pub profile_id: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AssignmentRevision {
    pub assignment_id: String,
    pub revision: u64,
    pub record: AssignmentRecord,
    pub committed_at: i64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn assignment_wire_uses_camel_case_and_roundtrips() {
        let record = AssignmentRecord {
            id: "a1".into(),
            owner_device_id: "host".into(),
            profile_id: "profile".into(),
            revision: 1,
            objective: "objective".into(),
            allowed_actions: vec![],
            linked_sessions: vec!["chat-1".into()],
            findings: vec![],
            evidence: vec![],
            reviews: vec![AssignmentReview {
                revision: 1,
                reviewer: "user".into(),
                outcome: "approved".into(),
                notes: "ok".into(),
            }],
            unresolved_questions: vec![],
        };
        let value = serde_json::to_value(&record).unwrap();
        assert_eq!(value["ownerDeviceId"], "host");
        assert_eq!(
            serde_json::from_value::<AssignmentRecord>(value).unwrap(),
            record
        );
    }
}
