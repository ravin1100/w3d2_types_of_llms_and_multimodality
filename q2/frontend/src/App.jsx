import { useState } from 'react'
import { ChakraProvider, Box, VStack, Heading, Text, Input, Button, Image, useToast, Textarea } from '@chakra-ui/react'
import ReactMarkdown from 'react-markdown'
import rehypeRaw from 'rehype-raw'
import { analyzeImage } from './api'
import './markdown.css'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const toast = useToast()

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
      setImagePreview(URL.createObjectURL(file))
    }
  }

  const handleSubmit = async () => {
    if (!selectedImage || !question) {
      toast({
        title: 'Error',
        description: 'Please select an image and enter a question',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
      return
    }

    setLoading(true)
    try {
      const result = await analyzeImage(selectedImage, question)
      setAnswer(result.answer)
      if (result.fallback) {
        toast({
          title: 'Notice',
          description: 'Image analysis failed. Using text-only response.',
          status: 'warning',
          duration: 5000,
          isClosable: true,
        })
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <ChakraProvider>
      <Box 
        minH="100vh" 
        w="100%" 
        bg="gray.50"
        py={8}
      >
        <Box 
          maxW="1200px" 
          w="90%" 
          mx="auto" 
          bg="white" 
          p={8} 
          borderRadius="xl" 
          boxShadow="lg"
        >
          <VStack spacing={8} align="stretch">
            <Heading textAlign="center" size="xl" mb={4}>Multimodal QA System</Heading>
            
            <Box 
              borderWidth={2} 
              borderRadius="xl" 
              p={6} 
              borderStyle="dashed" 
              borderColor="blue.200"
              bg="blue.50"
              _hover={{ borderColor: "blue.300", bg: "blue.100" }}
              transition="all 0.2s"
            >
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                style={{ display: 'none' }}
                id="image-upload"
              />
              <label htmlFor="image-upload">
                <Button 
                  as="span" 
                  width="full" 
                  mb={4}
                  size="lg"
                  colorScheme="blue"
                  variant="solid"
                >
                  Choose Image
                </Button>
              </label>
              
              {imagePreview && (
                <Image
                  src={imagePreview}
                  alt="Preview"
                  maxH="400px"
                  mx="auto"
                  objectFit="contain"
                  borderRadius="lg"
                  boxShadow="md"
                />
              )}
            </Box>

            <Textarea
              placeholder="Enter your question about the image..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              size="lg"
              minH="120px"
              p={4}
              borderRadius="lg"
              borderColor="gray.300"
              _hover={{ borderColor: "blue.300" }}
              _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px #3182CE" }}
            />

            <Button
              colorScheme="blue"
              onClick={handleSubmit}
              isLoading={loading}
              loadingText="Analyzing..."
              size="lg"
              height="60px"
              fontSize="xl"
            >
              Analyze Image
            </Button>

            {answer && (
              <Box 
                borderWidth={1} 
                borderRadius="xl" 
                p={6}
                bg="white"
                boxShadow="md"
              >
                <Text fontWeight="bold" fontSize="xl" mb={4}>Answer:</Text>
                <Box className="markdown-content">
                  <ReactMarkdown rehypePlugins={[rehypeRaw]}>
                    {answer}
                  </ReactMarkdown>
                </Box>
              </Box>
            )}
          </VStack>
        </Box>
      </Box>
    </ChakraProvider>
  )
}

export default App
