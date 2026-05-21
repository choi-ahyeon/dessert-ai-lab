import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    allowedDevOrigins: ['renovator-rubber-pony.ngrok-free.dev'],
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8000/:path*',
            },
        ]
    },
}

export default nextConfig