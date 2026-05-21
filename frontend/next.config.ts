import type { NextConfig } from "next";

/*레일*/
const nextConfig: NextConfig = {
    allowedDevOrigins: ['renovator-rubber-pony.ngrok-free.dev'],
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'https://dessert-ai-lab-production.up.railway.app/:path*',
            },
        ]
    },
}

export default nextConfig