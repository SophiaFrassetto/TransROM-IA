export interface User {
    id: number;
    email: string;
    name: string | null;
    picture: string | null;
    is_active: boolean;
    is_superuser: boolean;
    created_at: string;
    updated_at: string | null;
}

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterCredentials extends LoginCredentials {
    name: string;
    confirmPassword: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}
