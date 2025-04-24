# TransROM-IA Frontend

This is the frontend application for TransROM-IA, an AI-Assisted ROM Translation and Dubbing System.

## Getting Started

### Prerequisites

- Node.js 16.x or later
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Create a `.env.local` file in the root directory with the following content:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   │   └── layout/    # Layout components
│   ├── pages/         # Next.js pages
│   ├── store/         # Redux store
│   └── styles/        # CSS modules
├── public/            # Static assets
└── package.json       # Dependencies and scripts
```

## Features

- Modern UI with Material-UI components
- Responsive design
- TypeScript support
- Redux for state management
- Next.js for server-side rendering

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Contributing

Please follow the project's coding standards and submit pull requests to the main repository.

## License

This project is licensed under the MIT License. 