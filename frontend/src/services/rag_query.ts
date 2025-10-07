export interface RagQueryResponse {
    query: string;
    response?: {
        content: string;
        additional_kwargs: Record<string, unknown>;
        response_metadata: {
            prompt_feedback: {
                block_reason: number;
                safety_ratings: any[];
            };
            finish_reason: string;
            model_name: string;
            safety_ratings: any[];
        };
        type: string;
        name: string | null;
        id: string;
        example: boolean;
        tool_calls: any[];
        invalid_tool_calls: any[];
        usage_metadata: {
            input_tokens: number;
            output_tokens: number;
            total_tokens: number;
            input_token_details: Record<string, unknown>;
            output_token_details: Record<string, unknown>;
        };
    };
    context?: string[];
    error?: string;
    details?: string;
    fallback?: string;
}

export async function fetchRagQuery(q: string, k: number = 3): Promise<RagQueryResponse> {
    try {
        const params = new URLSearchParams({ q, k: k.toString() });
        const res = await fetch(`http://localhost:8000/rag_query?${params.toString()}`);
        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            return {
                query: q,
                error: errorData.error || 'Request failed',
                details: errorData.details || res.statusText,
                fallback: `Echo: ${q}`,
            };
        }
        return await res.json();
    } catch (error: any) {
        return {
            query: q,
            error: 'Request failed',
            details: error?.message,
            fallback: `Echo: ${q}`,
        };
    }
}
