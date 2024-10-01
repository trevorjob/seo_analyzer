from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import analyze_seo
from .models import Analysis
from .serializers import AnalysisSerializer


class AnalyzeSEO(APIView):
    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response(
                {"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Perform the SEO analysis
        seo_score, report = analyze_seo(url)

        # Save the analysis to the database
        analysis = Analysis.objects.create(url=url, seo_score=seo_score, report=report)
        serializer = AnalysisSerializer(analysis)

        return Response(serializer.data, status=status.HTTP_200_OK)
